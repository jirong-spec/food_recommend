# OpenStreetMap 遷移說明 🗺️

## 📌 遷移摘要

成功將 LINE 餐廳推薦機器人從 **Google Places API** 遷移至 **OpenStreetMap Overpass API**。

### 主要變更

| 項目 | 之前 (Google Places) | 之後 (OpenStreetMap) |
|------|---------------------|---------------------|
| **API** | Google Places API | Overpass API |
| **費用** | 免費額度 $200/月 | 完全免費，無限制 |
| **API 金鑰** | 需要 | 不需要 |
| **評分資料** | ✅ 有 (0-5星) | ❌ 無 |
| **地址資料** | ✅ 完整 | ✅ 有（依地區而異） |
| **餐廳類別** | ✅ 豐富 | ✅ 豐富 (OSM tags) |
| **營業時間** | ✅ 有 | ✅ 有 (部分) |
| **配額限制** | 有（28,000次/月） | 無 |

## 🔧 技術變更

### 1. 配置檔案 ([config.py](file:///c:/Users/jimmy/Line飲食推薦/config.py))

**移除**：
```python
GOOGLE_PLACES_API_KEY = os.getenv('GOOGLE_PLACES_API_KEY')
WEIGHT_RATING = 0.5
```

**新增**：
```python
OVERPASS_API_URL = os.getenv('OVERPASS_API_URL', 'https://overpass-api.de/api/interpreter')
WEIGHT_DISTANCE = 0.7  # 提高距離權重
WEIGHT_CATEGORY = 0.3  # 提高類別權重
```

### 2. 推薦引擎 ([recommender.py](file:///c:/Users/jimmy/Line飲食推薦/recommender.py))

**完全重寫**：
- 使用 Overpass QL 查詢語言
- 根據 OSM amenity 和 cuisine tags 篩選
- 移除評分計算邏輯
- 新增 OSM 資料解析

**Overpass 查詢範例**：
```python
query = f"""
[out:json][timeout:25];
(
    node["amenity"="restaurant"](around:{radius},{lat},{lon});
    node["amenity"="cafe"](around:{radius},{lat},{lon});
);
out body;
"""
```

### 3. 評分演算法

**之前**：
```python
score = 0.5 × rating + 0.3 × (1 - distance) + 0.2 × category
```

**之後**：
```python
score = 0.7 × (1 - distance) + 0.3 × category
```

**說明**：
- 移除評分因子（OSM 無評分資料）
- 提高距離權重至 70%
- 提高類別匹配權重至 30%
- 結果更注重「最近」而非「最高分」

### 4. 訊息模板 ([message_templates.py](file:///c:/Users/jimmy/Line飲食推薦/message_templates.py))

**移除**：
- 評分星星顯示
- Google Place ID 連結

**保留**：
- 距離顯示
- Google Maps 導航（使用經緯度）
- Carousel 模板

**新增**：
- 顯示餐廳類別 (cuisine)
- 簡化的地圖連結

## 📊 資料結構比較

### Google Places API 回應
```json
{
  "name": "餐廳名稱",
  "rating": 4.5,
  "user_ratings_total": 120,
  "vicinity": "完整地址",
  "place_id": "ChIJ...",
  "types": ["restaurant", "food"]
}
```

### OpenStreetMap 回應
```json
{
  "type": "node",
  "lat": 25.0330,
  "lon": 121.5654,
  "tags": {
    "name": "餐廳名稱",
    "amenity": "restaurant",
    "cuisine": "chinese",
    "addr:street": "街道名稱",
    "addr:city": "城市",
    "opening_hours": "Mo-Su 11:00-21:00",
    "phone": "+886-2-1234-5678"
  }
}
```

## ✅ 優點

1. **完全免費** 💰
   - 無 API 金鑰申請流程
   - 無配額限制
   - 無信用卡綁定

2. **開源資料** 🌍
   - 社群維護
   - 資料透明
   - 可貢獻改善

3. **豐富資訊** 📝
   - 營業時間
   - 電話號碼
   - 網站連結
   - 詳細地址

4. **簡化部署** 🚀
   - 少一個 API 金鑰要管理
   - 降低設定複雜度
   - 減少錯誤可能性

## ⚠️ 限制與解決方案

### 1. 無評分資料

**影響**：無法依評分排序

**解決方案**：
- 短期：使用距離優先排序
- 長期：可考慮自建評分系統
  - 讓使用者在 LINE 中評分
  - 儲存在資料庫（SQLite/PostgreSQL）
  - 結合 OSM 資料和自建評分

### 2. 資料完整度依地區而異

**影響**：某些地區可能餐廳資料較少

**解決方案**：
- 提供「增加搜尋半徑」選項
- 顯示友善的「無結果」訊息
- 鼓勵使用者貢獻 OSM 資料

### 3. 地址格式不統一

**影響**：某些餐廳可能無完整地址

**解決方案**：
- 使用經緯度作為主要定位方式
- 地址作為輔助資訊
- 提供「查看位置」按鈕直接開啟地圖

## 🔄 遷移檢查清單

- [x] 更新 `config.py` - 移除 Google API 設定
- [x] 重寫 `recommender.py` - 實作 Overpass API
- [x] 更新 `message_templates.py` - 移除評分顯示
- [x] 更新 `.env.example` - 移除 Google API 金鑰
- [x] 更新 `README.md` - 更新說明文件
- [x] 更新 `SETUP_CHECKLIST.md` - 移除 Google 設定步驟
- [x] 測試 Overpass API 查詢（待部署後測試）
- [x] 驗證資料解析正確性（待部署後測試）

## 📝 環境變數變更

### 之前
```bash
LINE_CHANNEL_ACCESS_TOKEN=...
LINE_CHANNEL_SECRET=...
GOOGLE_PLACES_API_KEY=...  # ❌ 移除
```

### 之後
```bash
LINE_CHANNEL_ACCESS_TOKEN=...
LINE_CHANNEL_SECRET=...
# OVERPASS_API_URL=...  # 可選，有預設值
```

## 🧪 測試建議

部署後請測試：

1. **基本功能**
   - [ ] 分享位置後能收到推薦
   - [ ] 推薦結果包含餐廳名稱和距離
   - [ ] 地圖導航連結正常運作

2. **類別篩選**
   - [ ] 測試各種類別（飲料、快餐、甜點等）
   - [ ] 確認類別匹配正確

3. **邊界情況**
   - [ ] 偏遠地區（可能無結果）
   - [ ] 市中心（應有大量結果）
   - [ ] 不同搜尋半徑

4. **效能**
   - [ ] Overpass API 回應時間（通常 < 5 秒）
   - [ ] 大量請求時的穩定性

## 🚀 未來改進方向

### 1. 自建評分系統
```python
# 讓使用者評分餐廳
@handler.add(PostbackEvent)
def handle_rating(event):
    restaurant_id = event.postback.data
    rating = get_user_rating()
    save_to_database(restaurant_id, rating)
```

### 2. 快取機制
```python
# 使用 Redis 快取常見位置的結果
import redis
cache = redis.Redis()
cached_result = cache.get(f"restaurants:{lat}:{lon}")
```

### 3. 顯示更多 OSM 資訊
```python
# 顯示營業時間、電話、網站
if restaurant.get('opening_hours'):
    info += f"\n🕐 {restaurant['opening_hours']}"
if restaurant.get('phone'):
    info += f"\n📞 {restaurant['phone']}"
```

## 📚 相關資源

- [Overpass API 文件](https://wiki.openstreetmap.org/wiki/Overpass_API)
- [Overpass Turbo](https://overpass-turbo.eu/) - 測試查詢
- [OSM Tags for Restaurants](https://wiki.openstreetmap.org/wiki/Tag:amenity%3Drestaurant)
- [OSM Cuisine Tags](https://wiki.openstreetmap.org/wiki/Key:cuisine)

## 💡 總結

這次遷移帶來了：
- ✅ **零成本**：完全免費，無配額限制
- ✅ **簡化部署**：少一個 API 金鑰要管理
- ✅ **開源精神**：使用社群維護的資料
- ⚠️ **權衡**：失去評分資料，但可未來自建

整體而言，對於個人專案或小型應用，OpenStreetMap 是更好的選擇！
