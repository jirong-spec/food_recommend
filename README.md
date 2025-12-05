# LINE 餐廳推薦機器人 🍴

一個基於 LINE Messaging API 的智能餐廳推薦系統，使用 OpenStreetMap 開源地圖資料，使用者只需分享位置，即可獲得附近餐廳推薦。

## ✨ 功能特色

- 📍 **位置智能推薦**：使用者分享位置後，自動搜尋附近餐廳
- 🌍 **開源地圖資料**：使用 OpenStreetMap，完全免費無額度限制
- 🎯 **類別篩選**：支援飲料、快餐、甜點、中式、日式、西式等多種類別
- 📏 **距離優先**：根據距離和類別匹配推薦最近的餐廳
- 🗺️ **一鍵導航**：直接連結 Google Maps 導航
- 💬 **友善介面**：使用 LINE Carousel 展示多家餐廳
- ☁️ **雲端部署**：部署在 Render 免費平台，24/7 運行

## 🏗️ 系統架構

```
使用者 (LINE App)
      ↓
LINE Messaging API
      ↓
Webhook (Render 雲端伺服器)
      ↓
Flask 後端
      ↓
OpenStreetMap Overpass API
      ↓
推薦演算法
      ↓
回傳 LINE 訊息
```

## 📋 前置需求

1. **LINE 官方帳號**
   - 前往 [LINE Developers Console](https://developers.line.biz/)
   - 建立 Messaging API Channel
   - 取得 Channel Access Token 和 Channel Secret

2. **Render 帳號**
   - 前往 [Render](https://render.com/) 註冊免費帳號

**注意**：不再需要 Google Places API！使用 OpenStreetMap 完全免費。

## 🚀 快速開始

### 1. 取得 LINE API 憑證

1. 前往 [LINE Developers Console](https://developers.line.biz/console/)
2. 建立新的 Provider（如果還沒有）
3. 建立 Messaging API Channel
4. 在 "Messaging API" 分頁中：
   - 取得 **Channel Secret**
   - 發行 **Channel Access Token**
   - 關閉 "Auto-reply messages"（自動回覆訊息）
   - 開啟 "Use webhooks"（使用 Webhook）

### 2. 部署到 Render

1. **Fork 或上傳程式碼到 GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **在 Render 建立 Web Service**
   - 登入 [Render Dashboard](https://dashboard.render.com/)
   - 點擊 "New +" → "Web Service"
   - 連結你的 GitHub repository
   - 設定如下：
     - **Name**: line-restaurant-bot（或任何名稱）
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app`
     - **Instance Type**: Free

3. **設定環境變數**
   
   在 Render 的 "Environment" 分頁中新增：
   ```
   LINE_CHANNEL_ACCESS_TOKEN=你的_Channel_Access_Token
   LINE_CHANNEL_SECRET=你的_Channel_Secret
   ```
   
   **注意**：不需要 Google API 金鑰！

4. **部署**
   - 點擊 "Create Web Service"
   - 等待部署完成（約 2-3 分鐘）
   - 記下你的 Render URL（例如：`https://line-restaurant-bot.onrender.com`）

### 3. 設定 LINE Webhook

1. 回到 [LINE Developers Console](https://developers.line.biz/console/)
2. 選擇你的 Messaging API Channel
3. 在 "Messaging API" 分頁中：
   - **Webhook URL**: 輸入 `https://你的render網址.onrender.com/callback`
   - 點擊 "Verify" 驗證（應該顯示 Success）
   - 開啟 "Use webhook"

### 4. 測試機器人

1. 用手機掃描 LINE Developers Console 中的 QR Code
2. 加入機器人為好友
3. 點擊「分享位置」按鈕
4. 選擇餐廳類別
5. 收到推薦餐廳！

## 💻 本地開發

```bash
# 1. 安裝相依套件
pip install -r requirements.txt

# 2. 建立 .env 檔案
cp .env.example .env
# 編輯 .env 填入你的 API 憑證

# 3. 執行 Flask 應用
python app.py

# 4. 使用 ngrok 建立公開 URL（用於測試 Webhook）
ngrok http 5000
# 將 ngrok 提供的 URL 設定到 LINE Webhook
```

## 🎯 使用方式

1. **加入機器人好友**：掃描 QR Code 或搜尋 LINE ID
2. **分享位置**：點擊「📍 分享我的位置」按鈕
3. **選擇類別**（可選）：選擇想要的餐廳類別
4. **查看推薦**：機器人會回傳附近最近的餐廳
5. **開啟導航**：點擊「🗺️ 開啟地圖導航」前往餐廳

## 🧮 推薦演算法

由於 OpenStreetMap 不提供評分資料，我們使用距離優先的演算法：

```python
score = 0.7 × (1 - distance_normalized) + 0.3 × category_match
```

- **distance_normalized**: 距離除以搜尋半徑（越近分數越高）
- **category_match**: 類別匹配（1=完全符合，0.5=部分符合，0=不符合）

**優點**：
- ✅ 完全免費，無 API 配額限制
- ✅ 開源資料，社群維護
- ✅ 包含豐富的餐廳資訊（名稱、地址、類別、營業時間等）

**限制**：
- ⚠️ 無評分資料（可考慮未來自建評分系統）
- ⚠️ 資料完整度依地區而異

## 📁 專案結構

```
Line飲食推薦/
├── app.py                 # Flask 主應用程式
├── config.py              # 配置管理
├── recommender.py         # 推薦引擎
├── message_templates.py   # LINE 訊息模板
├── utils.py               # 工具函數
├── requirements.txt       # Python 相依套件
├── Procfile              # Render 部署配置
├── runtime.txt           # Python 版本
├── .env.example          # 環境變數範例
├── .gitignore            # Git 忽略檔案
└── README.md             # 說明文件
```

## 🔧 配置選項

在 `.env` 檔案中可以調整以下參數：

```bash
# 搜尋半徑（公尺）
SEARCH_RADIUS=2000

# 最多推薦餐廳數量
MAX_RESULTS=5

# 距離權重
WEIGHT_DISTANCE=0.7

# 類別匹配權重
WEIGHT_CATEGORY=0.3
```

## 🐛 疑難排解

### Webhook 驗證失敗
- 確認 Render 部署成功（狀態為 "Live"）
- 確認 Webhook URL 正確（包含 `/callback`）
- 檢查環境變數是否正確設定

### 沒有收到推薦
- 確認已分享位置
- 檢查該地區 OpenStreetMap 是否有餐廳資料
- 嘗試增加搜尋半徑（修改 SEARCH_RADIUS）
- 查看 Render 的 Logs 是否有錯誤訊息

### 機器人沒有回應
- 確認 LINE Channel 的 Webhook 已開啟
- 確認已關閉「自動回覆訊息」
- 檢查 Render 服務是否正常運行

## 📊 服務限制

- **OpenStreetMap Overpass API**: 完全免費，無配額限制（請合理使用）
- **Render 免費版**: 750 小時/月，閒置 15 分鐘後休眠

## 🚀 未來功能

- [ ] 自建評分系統（讓使用者評分餐廳）
- [ ] 使用者偏好記憶（資料庫）
- [ ] 營業時間篩選（OSM 有此資料）
- [ ] 顯示餐廳電話和網站
- [ ] 收藏功能
- [ ] 推薦歷史記錄
- [ ] Rich Menu 快速選單
- [ ] 整合其他開源地圖資料

## 📝 授權

MIT License

## 👨‍💻 作者

Jimmy

## 🙏 致謝

- LINE Messaging API
- OpenStreetMap & Overpass API
- Render (雲端部署平台)
