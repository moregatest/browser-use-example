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
git clone [您的倉庫URL]
cd twitter-analyzer
```

2. 安裝依賴：
```bash
uv venv
source .venv/bin/activate  # Linux/macOS
# 或
.venv\Scripts\activate  # Windows
uv pip install -r requirements.txt
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
python twitter_reader.py [用戶名] --hours [小時數] --detailed
```

例如：
```bash
python twitter_reader.py elonmusk --hours 8 --detailed
```

參數說明：
- `用戶名`：要分析的 Twitter 用戶名（不需要包含 @）
- `--hours`：要分析的時間範圍（1-168小時）
- `--detailed`：是否使用詳細分析模式

## 注意事項

- 需要有效的 OpenAI API 金鑰
- 需要穩定的網絡連接
- Chrome 瀏覽器必須已安裝
