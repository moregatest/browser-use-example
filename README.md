# Twitter 分析工具

這是一個基於 Python 的 Twitter/X 推文分析工具，能夠自動抓取並分析特定用戶的最新推文。

## 功能特點

- 自動抓取指定用戶的最新推文
- 支援時間範圍過濾（1-168小時）
- 詳細分析模式，包含：
  - 推文內容分析
  - 圖片內容解析
  - 回覆分析
  - 互動數據統計
- 使用 GPT-4 進行智能分析
- 支援中文輸出

## 安裝需求

- Python 3.12+
- Chrome 瀏覽器
- OpenAI API 金鑰

## 安裝步驟

1. 克隆專案：
```bash
git clone https://github.com/moregatest/browser-use-example.git
cd browser-use-example
```

2. 安裝依賴：

此專案使用 uv 的腳本依賴管理，所以不需要手動安裝依賴。腳本會自動處理所需的套件。

需求：
- Python 3.12 或更高版本
- uv 套件管理器

如果還沒有安裝 uv，可以使用以下命令安裝：
```bash
pipx install uv
```

3. 設置環境變數：
創建 `.env` 文件並添加：
```
OPENAI_API_KEY=您的OpenAI API金鑰
OPENAI_API_URL=https://openrouter.ai/api/v1
```

## 使用方法

基本使用：
```bash
uv run twitter_reader.py [用戶名] --hours [小時數] --detailed
```

腳本會自動處理依賴套件的安裝，不需要手動安裝或創建虛擬環境。

### 運行範例

```bash
uv run twitter_reader.py JustinTrudeau --hours 8 --detailed
```

程式會輸出類似以下的分析結果：

```
在過去的8小時內，分析了@JustinTrudeau的推文，以下是詳細總結：

1. **主要話題：**
   - 與川普總統通話，討論加拿大的13億美元邊境計劃。
   - 增強邊境的直升機、技術和人員，以阻止芬太尼的流入。

2. **互動模式和趨勢：**
   - 第一條推文獲得了2.6萬次查看、3.2萬次轉推和13萬個喜歡。
   - 第二條推文獲得了828次查看、1,076次轉推和3,385個喜歡。

3. **重要公告或聲明：**
   - 加拿大政府將增強美加邊境的安全措施。

4. **社區反應和情感：**
   - 推文下的回覆顯示出對新邊境技術和合作的關注。
   - 社區對芬太尼的流入表示擔憶。
```

參數說明：
- `用戶名`：要分析的 Twitter 用戶名（不需要包含 @）
- `--hours`：要分析的時間範圍（1-168小時）
- `--detailed`：是否使用詳細分析模式

## 注意事項

- 需要有效的 OpenAI API 金鑰
- 需要穩定的網絡連接
- Chrome 瀏覽器必須已安裝
