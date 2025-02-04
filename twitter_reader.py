# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "python-dotenv",
#   "click",
#   "langchain-openai",
#   "browser-use",
#   "python-dateutil"
# ]
# ///

import os
import sys
from typing import Optional, List, Dict
from dataclasses import dataclass
from datetime import datetime, timedelta
from dateutil import parser
from dateutil.relativedelta import relativedelta

import click
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from langchain_openai import ChatOpenAI
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use import Agent, Browser


@dataclass
class TwitterConfig:
    """Configuration for Twitter reading"""
    openai_api_key: str
    openai_api_url: str
    chrome_path: str
    target_user: str  # Twitter handle without @
    time_window: int  # hours
    detailed_mode: bool
    headless: bool = False
    model: str = "openai/gpt-4o"
    base_url: str = "https://x.com"
    num_tweets_to_analyze: int = 10
    num_replies_to_analyze: int = 20


def get_chrome_user_data_dir() -> str:
    """取得Chrome用戶資料目錄"""
    home = os.path.expanduser("~")
    if sys.platform == "darwin":  # macOS
        return os.path.join(home, "Library", "Application Support", "Google", "Chrome")
    elif sys.platform == "win32":  # Windows
        return os.path.join(home, "AppData", "Local", "Google", "Chrome", "User Data")
    else:  # Linux
        return os.path.join(home, ".config", "google-chrome")

def create_config(target_user: str, time_window: int, detailed_mode: bool) -> TwitterConfig:
    """創建Twitter配置"""
    return TwitterConfig(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_api_url=os.getenv("OPENAI_API_URL"),
        chrome_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        target_user=target_user,
        time_window=time_window,
        detailed_mode=detailed_mode,
        headless=False,
        num_tweets_to_analyze=10  # 增加分析數量以確保能找到時間範圍內的推文
    )


def create_twitter_agent(config: TwitterConfig, browser: Browser) -> Agent:
    llm = ChatOpenAI(
        openai_api_base=config.openai_api_url,
        model=config.model,
        openai_api_key=config.openai_api_key,        
        temperature=0.7
    )
    
    base_task = f"""Navigate to Twitter and analyze tweets from user @{config.target_user} within the last {config.time_window} hours.

    Steps:
    1. Go to {config.base_url}/{config.target_user}
    2. Wait for the page to load completely
    3. Scroll down slowly to load tweets from the last {config.time_window} hours
    4. Check the timestamps of the first three tweets. If all of them are older than {config.time_window} hours, stop and respond with "No tweets found within the specified time window"
    5. For each tweet within the time window:
       - Read the content
       - Note the exact date and time
       - Check engagement metrics (likes, reposts, etc.)
       - Look for any media attachments
         * For images: analyze and describe the content, including any text, objects, or notable elements in the image
         * Include image content analysis in the overall tweet context
       - If in detailed mode, click on the tweet and analyze top {config.num_replies_to_analyze} replies
    6. Analyze the collected information and provide a detailed summary that includes:
       - Main topics discussed
       - Engagement patterns and trends
       - Notable announcements or statements
       - Community response and sentiment
       - Links to significant tweets
    7. Output your response in Taiwan chinese Language   

    Important:
    - Only analyze tweets from the last {config.time_window} hours
    - Include exact timestamps for all tweets
    - Note interactions with other users
    - Pay attention to threads and conversations
    - In detailed mode, analyze reply patterns and community sentiment
    - DO NOT "Click on the button to view replies" on tweets, just scroll down to view replies directly in the timeline
    """

    detailed_task = f"""
    For each analyzed tweet, also provide:
    - Top {config.num_replies_to_analyze} replies with their engagement metrics
    - Common themes in replies
    - Overall sentiment of responses
    - Notable disagreements or support
    - Influential users who responded
    """ if config.detailed_mode else ""

    return Agent(
        task=base_task + detailed_task,
        llm=llm,
        browser=browser,
    )


async def analyze_tweets(agent: Agent, browser: Browser, config: TwitterConfig):
    try:
        result = await agent.run(max_steps=200)  # 增加步驟上限以支援詳細模式
        
        print("\n=== 推文分析結果 ===")
        print("時間範圍：過去", config.time_window, "小時")
        if config.detailed_mode:
            print("模式：詳細分析（包含回覆）")
        else:
            print("模式：基本分析")
        print("-" * 50)
        print(result)
        
        return result
    except Exception as e:
        print(f"分析推文時發生錯誤: {str(e)}")
        return None
    finally:
        await browser.close()


@click.command()
@click.argument('username')
@click.option('--hours', '-h', default=24, help='分析最近幾小時內的推文 (預設: 24)')
@click.option('--detailed/--simple', '-d/-s', default=False, help='是否進行詳細分析，包含回覆 (預設: simple)')
def main(username: str, hours: int, detailed: bool):
    """分析特定用戶的推文

    USERNAME: 要分析的Twitter用戶名稱（不需要包含@）
    """
    if not os.getenv("OPENAI_API_KEY"):
        print("錯誤：需要設定 OPENAI_API_KEY 環境變數")
        return

    # 驗證時間範圍
    if hours <= 0 or hours > 168:  # 最多支援7天
        print("錯誤：時間範圍必須在 1 到 168 小時之間")
        return

    config = create_config(username, hours, detailed)
    
    # 使用已存在的Chrome profile
    user_data_dir = get_chrome_user_data_dir()
    print(f"使用Chrome設定檔目錄: {user_data_dir}")
    
    # 設定 Chrome 環境變數
    os.environ["CHROME_USER_DATA_DIR"] = user_data_dir
    os.environ["CHROME_PROFILE"] = "Profile 1"
    
    # 創建Browser實例
    browser = Browser(
        config=BrowserConfig(
            headless=config.headless,
            chrome_instance_path=config.chrome_path,
        )
    )
    agent = create_twitter_agent(config, browser)
    
    try:
        asyncio.run(analyze_tweets(agent, browser, config))
    except KeyboardInterrupt:
        print("\n程式已被使用者中斷")
    except Exception as e:
        print(f"\n執行時發生錯誤: {str(e)}")


if __name__ == "__main__":
    main()
