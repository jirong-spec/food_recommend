# 快速設定檢查清單 ✅

使用此清單確保所有步驟都已完成。

## 📋 部署前準備

### 1. LINE Messaging API 設定
- [ ] 前往 [LINE Developers Console](https://developers.line.biz/console/)
- [ ] 建立 Provider（如果沒有）
- [ ] 建立 Messaging API Channel
- [ ] 取得 **Channel Access Token**（記下來）
- [ ] 取得 **Channel Secret**（記下來）
- [ ] 關閉「自動回覆訊息」(Auto-reply messages)
- [ ] 開啟「使用 Webhook」(Use webhooks)

### 2. GitHub 設定
- [ ] 建立 GitHub repository
- [ ] 將程式碼推送到 GitHub
  ```bash
  cd Line飲食推薦
  git init
  git add .
  git commit -m "Initial commit"
  git branch -M main
  git remote add origin <your-repo-url>
  git push -u origin main
  ```

## 🚀 Render 部署

### 3. 建立 Web Service
- [ ] 登入 [Render](https://dashboard.render.com/)
- [ ] 點擊 "New +" → "Web Service"
- [ ] 連結 GitHub repository
- [ ] 設定名稱（例如：line-restaurant-bot）
- [ ] 選擇 Python 3 環境
- [ ] Build Command: `pip install -r requirements.txt`
- [ ] Start Command: `gunicorn app:app`
- [ ] 選擇 Free 方案

### 4. 設定環境變數
在 Render 的 Environment 分頁新增：

- [ ] `LINE_CHANNEL_ACCESS_TOKEN` = _你的 Channel Access Token_
- [ ] `LINE_CHANNEL_SECRET` = _你的 Channel Secret_

**注意**：不需要 Google API 金鑰！使用 OpenStreetMap 完全免費。

### 5. 部署
- [ ] 點擊 "Create Web Service"
- [ ] 等待部署完成（約 2-3 分鐘）
- [ ] 確認狀態為 "Live"（綠色）
- [ ] 記下 Render URL（例如：`https://line-restaurant-bot.onrender.com`）

## 🔗 LINE Webhook 設定

### 6. 設定 Webhook URL
- [ ] 回到 LINE Developers Console
- [ ] 選擇你的 Messaging API Channel
- [ ] 在 "Messaging API" 分頁找到 "Webhook settings"
- [ ] Webhook URL 輸入：`https://你的render網址.onrender.com/callback`
- [ ] 點擊 "Update"
- [ ] 點擊 "Verify"
- [ ] 確認顯示 "Success" ✅
- [ ] 確認 "Use webhook" 開關是**開啟**的

## 🧪 測試

### 7. 測試機器人
- [ ] 用手機掃描 LINE Developers Console 的 QR Code
- [ ] 加入機器人為好友
- [ ] 應該收到歡迎訊息
- [ ] 點擊「📍 分享我的位置」
- [ ] 分享你的位置
- [ ] 應該收到附近餐廳推薦（Carousel 訊息）
- [ ] 點擊「🗺️ 開啟地圖導航」測試導航功能
- [ ] 測試選擇不同類別（飲料、快餐、甜點等）

## 🐛 如果遇到問題

### Webhook 驗證失敗
- [ ] 確認 Render 服務狀態是 "Live"
- [ ] 確認 Webhook URL 包含 `/callback`
- [ ] 檢查環境變數是否正確
- [ ] 查看 Render Logs 是否有錯誤

### 機器人沒有回應
- [ ] 確認 "Use webhook" 已開啟
- [ ] 確認 "Auto-reply messages" 已關閉
- [ ] 檢查 Render Logs
- [ ] 確認 LINE Channel Access Token 正確

### 沒有收到推薦
- [ ] 確認已分享位置
- [ ] 檢查該地區 OpenStreetMap 是否有餐廳資料
- [ ] 嘗試增加搜尋半徑（修改 SEARCH_RADIUS 環境變數）
- [ ] 查看 Render Logs 的錯誤訊息

## 📊 監控

### 8. 設定監控（可選）
- [ ] 註冊 [UptimeRobot](https://uptimerobot.com/)
- [ ] 新增監控：`https://你的服務名稱.onrender.com/`
- [ ] 設定每 5 分鐘檢查一次（避免休眠）

## ✅ 完成！

恭喜！你的 LINE 餐廳推薦機器人已經上線了！🎉

### 下一步
- 分享給朋友測試
- 調整推薦演算法權重（在 Render 環境變數中）
- 查看使用情況（Render Logs）
- 考慮新增更多功能（參考 README.md 的未來功能清單）

## 📞 需要幫助？

查看詳細文件：
- [README.md](file:///c:/Users/jimmy/Line飲食推薦/README.md) - 完整使用指南
- [DEPLOYMENT.md](file:///c:/Users/jimmy/Line飲食推薦/DEPLOYMENT.md) - 詳細部署說明
