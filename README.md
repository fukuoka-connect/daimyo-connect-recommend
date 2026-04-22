# DAIMYOU CONNECT RECOMMEND MAP

ラジオ番組「DAIMYOU CONNECT」に縁のある飲食店・バー・ショップを地図で辿る、福岡の観光レコメンドMAP。

## ライブ版

- 本番: https://daimyo-connect-recommend.vercel.app/
- ミラー: https://fukuoka-connect.github.io/daimyo-connect-recommend/

## 特徴

- 🗺️ 地図上で店舗を視覚的に探索（Leaflet + CartoDB）
- 📍 エリア・ジャンル別のフィルタ
- 🪟 店舗詳細パネル（営業時間・SNS・Web・推薦理由・関連店舗）
- 🔗 店舗同士の「つながり」をたどれる構造
- 📱 スマホ最適化

## データ構造

`data.json` で全データ管理：

- `shops`: 各店舗の情報（ジャンル・タグ・営業時間・SNS・関連店舗）
- `connections`: 店舗間の関係性（エリア・店主仲良し・姉妹店 など）
- `categories`: ジャンル・タグのマスタ

## 今後の展開

- **Phase 1** (現状): 地図 + 詳細パネル + エリア/ジャンルフィルタ
- **Phase 2**: 店主コメント・フォトギャラリー
- **Phase 3**: NETWORK タブ（Cytoscape.js で店舗間のつながりをObsidian風グラフ表示）
- **Phase 4**: admin.html 拡張（GUI で関係性エッジ編集）
- **Phase 5**: Google Maps API 切替判断（トラフィックが増えたら）

## 技術スタック

- HTML / CSS / JavaScript（フレームワーク不使用）
- [Leaflet.js](https://leafletjs.com/) 1.9.4（地図）
- CartoDB voyager_labels_under タイル
- Google Fonts（Shippori Mincho, Zen Kaku Gothic New）
- Vercel ホスティング

---

Powered by [Fukuoka Connect](https://fukuoka-connect.github.io/)
