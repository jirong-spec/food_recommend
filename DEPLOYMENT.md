# Render 部署詳細指南

本文件提供 LINE 餐廳推薦機器人在 Render 平台上的詳細部署步驟。

## 📋 部署前準備

### 1. 確認已完成

- ✅ 已取得 LINE Channel Access Token
- ✅ 已取得 LINE Channel Secret
- ✅ 已取得 Google Places API Key
- ✅ 程式碼已上傳到 GitHub

### 2. 建立 GitHub Repository

如果還沒有上傳程式碼到 GitHub：

```bash
# 初始化 Git repository
cd Line飲食推薦
git init

# 新增所有檔案
git add .

# 提交
git commit -m "Initial commit: LINE Restaurant Bot"

# 建立 GitHub repository 後，連結並推送
git branch -M main
git remote add origin https://github.com/你的使用者名稱/line-restaurant-bot.git
git push -u origin main
```

## 🚀 Render 部署步驟

### 步驟 1: 建立 Render 帳號

1. 前往 [Render](https://render.com/)
2. 點擊 "Get Started" 或 "Sign Up"
3. 使用 GitHub 帳號登入（推薦）或使用 Email 註冊

### 步驟 2: 建立 Web Service

1. 登入後，進入 [Dashboard](https://dashboard.render.com/)
2. 點擊右上角 "New +" 按鈕
3. 選擇 "Web Service"

### 步驟 3: 連結 GitHub Repository

1. 如果是第一次使用，需要授權 Render 存取 GitHub
2. 在 repository 列表中找到 `line-restaurant-bot`
3. 點擊 "Connect"

### 步驟 4: 配置 Web Service

填寫以下設定：

#### Basic Settings
- **Name**: `line-restaurant-bot`（或任何你喜歡的名稱）
- **Region**: 選擇 `Singapore` 或 `Oregon`（離台灣較近）
- **Branch**: `main`
- **Root Directory**: 留空（如果程式碼在根目錄）

#### Build & Deploy
- **Runtime**: `Python 3`
- **Build Command**: 
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command**: 
  ```bash
  gunicorn app:app
  ```

#### Instance Type
- 選擇 **Free**（免費方案）

### 步驟 5: 設定環境變數

在 "Environment" 分頁中，點擊 "Add Environment Variable"，新增以下變數：

| Key | Value |
|-----|-------|
| `LINE_CHANNEL_ACCESS_TOKEN` | 你的 LINE Channel Access Token |
| `LINE_CHANNEL_SECRET` | 你的 LINE Channel Secret |
| `GOOGLE_PLACES_API_KEY` | 你的 Google Places API Key |

可選配置（使用預設值也可以）：
| Key | Value | 說明 |
|-----|-------|------|
| `SEARCH_RADIUS` | `2000` | 搜尋半徑（公尺） |
| `MAX_RESULTS` | `5` | 最多推薦數量 |
| `WEIGHT_RATING` | `0.5` | 評分權重 |
| `WEIGHT_DISTANCE` | `0.3` | 距離權重 |
| `WEIGHT_CATEGORY` | `0.2` | 類別權重 |

### 步驟 6: 部署

1. 確認所有設定正確
2. 點擊 "Create Web Service"
3. Render 會開始建置和部署（約 2-3 分鐘）
4. 等待狀態變成 "Live"（綠色）

### 步驟 7: 取得 Webhook URL

部署成功後：
1. 在 Service 頁面上方可以看到你的 URL
2. 格式：`https://你的服務名稱.onrender.com`
3. 完整的 Webhook URL：`https://你的服務名稱.onrender.com/callback`

### 步驟 8: 設定 LINE Webhook

1. 前往 [LINE Developers Console](https://developers.line.biz/console/)
2. 選擇你的 Messaging API Channel
3. 點擊 "Messaging API" 分頁
4. 找到 "Webhook settings"：
   - **Webhook URL**: 輸入 `https://你的服務名稱.onrender.com/callback`
   - 點擊 "Update"
   - 點擊 "Verify" 驗證
   - 應該會顯示 "Success" ✅
5. 確認 "Use webhook" 開關是**開啟**的
6. 確認 "Auto-reply messages" 是**關閉**的

### 步驟 9: 測試

1. 用手機掃描 LINE Developers Console 中的 QR Code
2. 加入機器人為好友
3. 應該會收到歡迎訊息
4. 點擊「📍 分享我的位置」
5. 分享位置後應該會收到餐廳推薦

## 🔍 檢查部署狀態

### 查看 Logs

1. 在 Render Dashboard 中，點擊你的 Service
2. 點擊 "Logs" 分頁
3. 可以看到即時的應用程式日誌

### 測試 Health Check

在瀏覽器中開啟：
```
https://你的服務名稱.onrender.com/
```

應該會看到：
```
LINE Restaurant Bot is running! 🍴
```

## ⚠️ 重要注意事項

### Render 免費版限制

1. **休眠機制**：
   - 閒置 15 分鐘後會自動休眠
   - 下次請求時需要 30-60 秒喚醒
   - 第一次回應可能較慢

2. **運行時數**：
   - 免費版每月 750 小時
   - 足夠個人使用

3. **效能限制**：
   - 共享 CPU 和記憶體
   - 適合小型專案和測試

### 避免休眠的方法

可以使用外部服務定期 ping 你的應用：

1. **UptimeRobot**（推薦）
   - 前往 [UptimeRobot](https://uptimerobot.com/)
   - 建立免費帳號
   - 新增監控：`https://你的服務名稱.onrender.com/`
   - 設定每 5 分鐘檢查一次

2. **Cron-job.org**
   - 前往 [Cron-job.org](https://cron-job.org/)
   - 建立定時任務
   - 每 10 分鐘訪問你的 URL

## 🔄 更新部署

### 自動部署

Render 預設會自動部署：
1. 推送程式碼到 GitHub
   ```bash
   git add .
   git commit -m "Update feature"
   git push
   ```
2. Render 會自動偵測並重新部署

### 手動部署

1. 在 Render Dashboard 中
2. 點擊 "Manual Deploy" → "Deploy latest commit"

## 🐛 疑難排解

### 部署失敗

**檢查項目**：
- ✅ `requirements.txt` 檔案存在且格式正確
- ✅ `Procfile` 檔案存在
- ✅ `runtime.txt` 指定的 Python 版本正確
- ✅ 查看 Logs 中的錯誤訊息

### Webhook 驗證失敗

**可能原因**：
1. 環境變數設定錯誤
   - 重新檢查 `LINE_CHANNEL_SECRET` 是否正確
2. 服務尚未完全啟動
   - 等待 1-2 分鐘後再試
3. URL 輸入錯誤
   - 確認包含 `/callback`

### 機器人沒有回應

**檢查清單**：
1. ✅ Render 服務狀態是 "Live"
2. ✅ Webhook 驗證成功
3. ✅ "Use webhook" 已開啟
4. ✅ "Auto-reply messages" 已關閉
5. ✅ 環境變數都已正確設定
6. ✅ 查看 Render Logs 是否有錯誤

### Google Places API 錯誤

**常見問題**：
1. API 金鑰無效
   - 重新檢查 Google Cloud Console
2. Places API 未啟用
   - 確認已啟用 Places API
3. 超過配額
   - 檢查 Google Cloud Console 的配額使用情況

## 💰 成本估算

### 免費方案

- **Render**: 免費（750 小時/月）
- **Google Places API**: 免費額度 $200/月
- **LINE Messaging API**: 免費

### 預估使用量

假設每天 100 次推薦請求：
- Google Places API: 100 次 × 30 天 = 3,000 次/月
- 成本: 約 $10-15 USD（遠低於 $200 免費額度）

## 🎯 下一步

部署成功後，你可以：

1. **分享給朋友**：讓他們加入機器人測試
2. **監控使用情況**：查看 Render Logs 和 Google API 配額
3. **新增功能**：參考 README 中的未來功能清單
4. **優化效能**：調整推薦演算法權重

## 📚 相關資源

- [Render 官方文件](https://render.com/docs)
- [LINE Messaging API 文件](https://developers.line.biz/en/docs/messaging-api/)
- [Google Places API 文件](https://developers.google.com/maps/documentation/places/web-service)
