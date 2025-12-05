# 部署錯誤修復指南 🔧

## 問題描述

部署時出現 Python 3.13 與 `aiohttp` 套件的相容性錯誤：
```
error: 'PyLongObject' has no member named 'ob_digit'
```

## 原因

- `runtime.txt` 原本指定 Python 3.11.6
- Render 自動升級到 Python 3.13.4
- Python 3.13 有 breaking changes，導致 `line-bot-sdk` 的依賴套件 `aiohttp` 編譯失敗

## 解決方案

已更新 `runtime.txt` 為 `python-3.11.9`（Python 3.11 的最新穩定版）

## 部署步驟

### 1. 推送修復到 GitHub

```bash
cd Line飲食推薦

# 確認變更
git status

# 加入變更
git add runtime.txt

# 提交
git commit -m "Fix: Update Python to 3.11.9 for aiohttp compatibility"

# 推送到 GitHub
git push origin main
```

### 2. Render 自動重新部署

推送後，Render 會自動偵測到變更並重新部署。

### 3. 監控部署狀態

1. 前往 [Render Dashboard](https://dashboard.render.com/)
2. 選擇你的 Web Service
3. 查看 "Events" 或 "Logs" 分頁
4. 等待部署完成（約 2-3 分鐘）
5. 確認狀態變成 "Live" (綠色)

### 4. 驗證部署

在瀏覽器開啟：
```
https://你的服務名稱.onrender.com/
```

應該看到：
```
LINE Restaurant Bot is running! 🍴
```

## 如果還是失敗

### 方案 A：手動觸發重新部署

1. 在 Render Dashboard 中
2. 點擊 "Manual Deploy" → "Clear build cache & deploy"
3. 等待重新建置

### 方案 B：檢查 Python 版本

確認 `runtime.txt` 內容為：
```
python-3.11.9
```

### 方案 C：降級 line-bot-sdk（不建議）

如果上述方法都失敗，可以嘗試降級：
```
line-bot-sdk==3.4.0
```

## 預防措施

### 鎖定 Python 版本

在 `runtime.txt` 中明確指定版本，避免自動升級：
```
python-3.11.9
```

### 定期更新依賴

每隔幾個月檢查並更新套件版本：
```bash
pip list --outdated
pip install --upgrade line-bot-sdk
```

## 相關資源

- [Render Python 版本支援](https://render.com/docs/python-version)
- [Python 3.13 Release Notes](https://docs.python.org/3/whatsnew/3.13.html)
- [line-bot-sdk Issues](https://github.com/line/line-bot-sdk-python/issues)

## 快速指令

```bash
# 一鍵推送修復
cd Line飲食推薦
git add runtime.txt
git commit -m "Fix Python version compatibility"
git push origin main
```

部署成功後，記得測試 LINE Bot 功能！
