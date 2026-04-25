# CLAUDE.md — DAIMYOU CONNECT RECOMMEND
# Figma MCP 統合・設計システム ルールドキュメント

---

## 1. プロジェクト概要

| 項目 | 内容 |
|---|---|
| サイト名 | DAIMYOU CONNECT RECOMMEND |
| URL | https://daimyo-connect-recommend.vercel.app |
| 構成 | Pure HTML + CSS + Vanilla JS（フレームワークなし） |
| デプロイ | Vercel（GitHub 自動デプロイ） |
| ページ数 | 3ページ（index.html / shops.html / shop.html） |
| データ | `/data/curator.json`, `/data/shops.json` |

---

## 2. デザイントークン（CSS カスタムプロパティ）

全ページの `<style>` 内 `:root` に定義。共有 CSS ファイルなし（各ページに複製）。

### カラートークン

```css
:root {
  /* Backgrounds */
  --bg:          #0c0a10;   /* ページ背景（極暗パープル黒）*/
  --bg-2:        #13101b;   /* セカンダリ背景 */
  --surface:     #1a1626;   /* カード・セクション背景 */
  --surface-2:   #221d30;   /* プレースホルダー・深い面 */

  /* Borders */
  --border:      rgba(200,150,60,0.15);  /* アンバー縁（カード等）*/
  --border-dim:  rgba(255,255,255,0.06); /* ほぼ不可視の区切り線 */

  /* Text */
  --text:        #f0ebe0;   /* メインテキスト（温かみのあるオフホワイト）*/
  --text-mid:    #a08a6e;   /* サブテキスト */
  --text-dim:    #5a4e42;   /* 薄いラベル・プレースホルダー */

  /* Accents */
  --accent:      #c8963c;   /* 琥珀・主アクセント（CTA・ラベル・強調）*/
  --accent-warm: #dfa83c;   /* ホバー時・明るいアクセント */
  --red:         #7d2030;   /* 深い赤（セカンダリアクセント）*/
}
```

### エリアカラー（マップピン・カードアクセントバー）

JS オブジェクトとして各ページに定義：

```js
const AREA_COLORS = {
  '大名':      '#c8963c',
  '薬院':      '#e07850',
  '博多冷泉町': '#4a96c8',
  '野間大池':   '#5a9e58',
  '野間四角':   '#6eb86e',
  '宇美町':    '#a85ab4',
  '唐津':      '#46b4a0',
};
```

**Figma からカラーを受け取る場合**: 上記 CSS 変数・エリアカラーに対応する Figma トークン名を使用すること。新しいカラーを追加する際は `:root` と `AREA_COLORS` の両方を更新。

---

## 3. タイポグラフィ

### フォントスタック

```css
/* 見出し（和文セリフ） */
font-family: 'Shippori Mincho', serif;

/* 本文（和文ゴシック） */
font-family: 'Noto Sans JP', sans-serif;

/* 英字装飾・ロゴ */
font-family: 'Cormorant Garamond', serif;
```

Google Fonts CDN から読み込み：
```html
<link href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@400;600;700;800&family=Noto+Sans+JP:wght@300;400;500;700&family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400;1,600&display=swap" rel="stylesheet">
```

### タイプスケール

| 用途 | サイズ | フォント | ウェイト |
|---|---|---|---|
| ヒーロー見出し | `clamp(2.2rem, 8vw, 3.8rem)` | Shippori Mincho | 800 |
| セクション見出し | `1.5rem` | Shippori Mincho | 700 |
| 店舗名（カード） | `1.05rem` | Shippori Mincho | 700 |
| ナッツコメント本文 | `1rem` | Shippori Mincho | 400 |
| 本文 | `0.92rem` | Noto Sans JP | 400 |
| キャプション・タグ | `0.75rem` | Noto Sans JP | 500 |
| ロゴ | `1.1rem` | Cormorant Garamond | 600 |
| セクションラベル（EN） | `0.7rem` | Cormorant Garamond | 600 |

---

## 4. コンポーネントパターン

コンポーネントは独立したファイルではなく、各 HTML ページ内に CSS クラスとして定義。

### 4-1. アバター（円形プレースホルダー）

```html
<div class="avatar avatar-64">N</div>
<div class="avatar avatar-80">N</div>
<div class="avatar avatar-40">N</div>
```

```css
.avatar {
  border-radius: 50%;
  background: linear-gradient(135deg, var(--accent), var(--accent-warm));
  display: flex; align-items: center; justify-content: center;
  font-family: 'Cormorant Garamond', serif;
  font-weight: 600;
  color: var(--bg);
  border: 2px solid rgba(200,150,60,0.3);
}
.avatar-64 { width: 64px; height: 64px; font-size: 1.5rem; }
.avatar-80 { width: 80px; height: 80px; font-size: 1.8rem; }
.avatar-40 { width: 40px; height: 40px; font-size: 1rem; }
```

**Figma 対応**: 実写真は `<img>` に差し替え。`photo` が `null` の間はアバターを維持。

### 4-2. 店舗カード（一覧・プレビュー用）

```html
<a href="shop.html?id=xxx" class="shop-card">
  <div class="shop-card-photo" style="--area-color:#c8963c">
    <!-- placeholder or img -->
  </div>
  <div class="area-bar" style="background:#c8963c"></div>
  <div class="shop-card-body">
    <div class="shop-tags">
      <span class="tag area-tag">大名</span>
      <span class="tag">バー</span>
    </div>
    <div class="shop-card-name">晩酌bar ONEDAY</div>
    <div class="shop-card-comment">ナッツのショートコメント</div>
  </div>
</a>
```

エリアカラーは `style` 属性でインライン適用（`AREA_COLORS` から JS で注入）。

### 4-3. 店舗写真プレースホルダー（4:3）

```css
.shop-card-photo {
  aspect-ratio: 4/3;
  background: var(--surface-2);
  /* 斜線テクスチャ */
  background-image: repeating-linear-gradient(
    -45deg, transparent, transparent 3px,
    rgba(255,255,255,0.015) 3px, rgba(255,255,255,0.015) 6px
  );
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
}
```

**Figma から実写真を受け取る場合**: `photos[]` 配列に画像パスを追加するだけで `<img>` に自動切替。

### 4-4. ナッツコメント枠（shop.html のメインコンテンツ）

```html
<div class="nuts-comment">
  <div class="nuts-comment-header">🎤 ナッツのおすすめ</div>
  <div class="nuts-comment-body">
    <div class="avatar avatar-40">N</div>
    <div class="nuts-comment-text">コメント本文...</div>
  </div>
  <div class="nuts-comment-sig">— ナッツ</div>
</div>
```

左に 3px amber ボーダー、`--surface` 背景。視覚的にページの主役。

### 4-5. タグ

```html
<span class="tag">居酒屋</span>
<span class="tag area-tag">大名</span>  <!-- area-tag はアクセントカラー縁 -->
```

```css
.tag {
  font-size: 0.72rem; font-weight: 500;
  padding: 3px 8px; border-radius: 2px;
  background: var(--surface-2);
  color: var(--text-mid);
  border: 1px solid var(--border-dim);
}
.tag.area-tag {
  background: transparent;
  border-color: var(--accent);
  color: var(--accent);
}
```

### 4-6. CTAボタン

```html
<a href="shops.html" class="btn-primary">14の店を見る →</a>
```

```css
.btn-primary {
  background: var(--accent); color: var(--bg);
  font-weight: 700; padding: 16px 28px;
  border-radius: 2px; text-decoration: none;
  transition: background 0.2s, transform 0.2s;
}
.btn-primary:hover { background: var(--accent-warm); transform: translateY(-2px); }
```

### 4-7. セクションラベル

```html
<div class="section-label">Curator's Pick</div>
```

```css
.section-label {
  font-family: 'Cormorant Garamond', serif;
  font-size: 0.7rem; font-weight: 600;
  letter-spacing: 0.35em; text-transform: uppercase;
  color: var(--accent);
  display: flex; align-items: center; gap: 10px;
}
.section-label::before {
  content: ''; width: 24px; height: 1px; background: var(--accent);
}
```

---

## 5. レイアウト・スペーシング

### コンテナ幅

```css
max-width: 640px;   /* 全ページのコンテンツ幅上限 */
margin: 0 auto;
padding: 0 24px;    /* 左右余白（モバイル）*/
```

マップのみ `max-width: 100%`（full-width）。

### スペーシングスケール（使用パターン）

| 用途 | 値 |
|---|---|
| セクション間 | `64px` / `80px` |
| カード内パディング | `20px` / `24px` |
| カード間ギャップ | `12px` / `14px` |
| タグ間ギャップ | `6px` / `8px` |
| ヘッダー高さ | `56px` |

### ヘッダー（sticky、全ページ共通）

```css
.site-header {
  position: sticky; top: 0; z-index: 100;
  height: 56px;
  background: rgba(12,10,16,0.92);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border-dim);
}
```

---

## 6. ページ構成

```
daimyo-connect-recommend/
├── index.html          # トップ（ヒーロー・哲学・キュレーター紹介・店舗プレビュー）
├── shops.html          # 一覧（Leaflet地図 / リスト切替・フィルター）
├── shop.html           # 詳細（?id=xxx クエリパラメータでデータ特定）
├── data/
│   ├── curator.json    # ナッツのプロフィール・哲学テキスト
│   └── shops.json      # 14店舗データ（coordinates, nutsComment, owner 等）
├── data.json           # 旧バージョンのデータ（使用しない）
├── form/               # 店舗情報フォーム（触れない）
│   ├── index.html
│   └── qr/
└── CLAUDE.md           # このファイル
```

---

## 7. データスキーマ

### curator.json

```json
{
  "name": "ナッツ",
  "nameEn": "NUTS",
  "role": "DAIMYOU CONNECT 主宰 / ラジオパーソナリティ",
  "profession": "ダクト屋",
  "photo": null,                    // null = アバタープレースホルダー表示
  "photoPlaceholder": "N",          // アバターのイニシャル
  "bio": "...",
  "shortBio": "...",
  "philosophy": "...",              // フィロソフィーセクションのテキスト
  "eventUrl": "https://..."
}
```

### shops.json（1店舗のスキーマ）

```json
{
  "id": "oneday",                   // URL パラメータ: shop.html?id=oneday
  "name": "晩酌bar ONEDAY",
  "area": "大名",                   // AREA_COLORS のキーと一致させる
  "genre": "バー",
  "address": "...",
  "googleMapUrl": "https://...",
  "instagram": "oneday_banshakubar",
  "instagramUrl": "https://...",
  "phone": null,                    // null = 電話ボタン非表示
  "hours": "21:00〜翌3:00",
  "closedDays": null,
  "website": null,                  // null = サイトボタン非表示
  "coordinates": { "lat": 33.58, "lng": 130.39 },
  "photos": [],                     // 空 = プレースホルダー。パス追加で即反映
  "nutsComment": {
    "short": "30字以内のショートコメント",
    "long":  "100〜200字のロングコメント"
  },
  "owner": {
    "name": null,                   // null = オーナーセクション非表示
    "photo": null,
    "photoPlaceholder": "O",
    "bio": null
  }
}
```

---

## 8. JavaScript パターン

### XSS 対策（必須）

```js
function escHtml(s) {
  if (!s) return '';
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}
```

DOM へのすべての文字列挿入に使用。`innerHTML` を使う場合は必ず `escHtml()` を通すこと。

### データ取得

```js
const [curatorRes, shopsRes] = await Promise.all([
  fetch('/data/curator.json'),
  fetch('/data/shops.json'),
]);
const curator = await curatorRes.json();
const { shops } = await shopsRes.json();
```

### スクロールフェードイン

```js
const obs = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('visible'); obs.unobserve(e.target); }
  });
}, { threshold: 0.1 });
document.querySelectorAll('.fade-in').forEach(el => obs.observe(el));
```

```css
.fade-in { opacity: 0; transform: translateY(16px); transition: opacity 0.6s, transform 0.6s; }
.fade-in.visible { opacity: 1; transform: none; }
```

### 横スクロール（プレビュー・近隣店舗）

```css
.scroll-row {
  display: flex; gap: 14px;
  overflow-x: auto; scroll-snap-type: x mandatory;
  padding-bottom: 4px;
}
.scroll-row::-webkit-scrollbar { display: none; }
.scroll-row > * { scroll-snap-align: start; flex-shrink: 0; }
```

---

## 9. 地図（Leaflet）

```html
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" ...>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" ...></script>
```

タイル: **CartoDB Dark Matter Labels**（ダークテーマに合わせた暗いマップ）

```js
L.tileLayer(
  'https://{s}.basemaps.cartocdn.com/dark_matter_labels/{z}/{x}/{y}{r}.png',
  { attribution: '© OpenStreetMap © CARTO', maxZoom: 19 }
).addTo(map);
```

ピンは `L.divIcon` で円形カスタムアイコン（エリアカラー背景 + 店名イニシャル）。

---

## 10. アセット管理

現在、すべての画像は**プレースホルダー**（CSS で生成）。

将来の実写真追加ルール：
- ナッツ写真: `curator.json` の `"photo": "images/nuts/nuts.jpg"` を更新
- 店舗写真: `shops.json` の `"photos": ["images/shops/oneday-1.jpg"]` に追加
- オーナー写真: `shops.json` の `"owner.photo": "images/owners/oneday-owner.jpg"` に追加
- ファイル配置: `/public/images/` 配下（Vercel は `/public` を静的配信）

---

## 11. Figma からコードに変換する際のルール

### カラー対応表

| Figma トークン名（推奨） | CSS 変数 | Hex |
|---|---|---|
| `color/bg/primary` | `--bg` | `#0c0a10` |
| `color/bg/secondary` | `--bg-2` | `#13101b` |
| `color/surface/default` | `--surface` | `#1a1626` |
| `color/surface/raised` | `--surface-2` | `#221d30` |
| `color/text/primary` | `--text` | `#f0ebe0` |
| `color/text/secondary` | `--text-mid` | `#a08a6e` |
| `color/text/disabled` | `--text-dim` | `#5a4e42` |
| `color/accent/amber` | `--accent` | `#c8963c` |
| `color/accent/amber-warm` | `--accent-warm` | `#dfa83c` |
| `color/accent/red` | `--red` | `#7d2030` |

### Figma コンポーネント → HTML クラス対応

| Figma コンポーネント | HTML クラス | ファイル |
|---|---|---|
| Avatar/Small | `.avatar.avatar-40` | 全ページ |
| Avatar/Medium | `.avatar.avatar-64` | index.html |
| Avatar/Large | `.avatar.avatar-80` | index.html |
| ShopCard/Preview | `.shop-card` | index.html, shops.html |
| Tag/Area | `.tag.area-tag` | 全ページ |
| Tag/Genre | `.tag` | 全ページ |
| Button/Primary | `.btn-primary` | 全ページ |
| SectionLabel | `.section-label` | index.html, shop.html |
| NutsComment | `.nuts-comment` | shop.html |

### 新コンポーネントを追加する場合

1. CSS は当該ページの `<style>` 内に追記
2. JS でのレンダリングは `escHtml()` を必ず使用
3. 画像は `photo` フィールドが `null` の場合プレースホルダーを表示するロジックを維持
4. `data/shops.json` のスキーマ変更は全ページの JS に影響するため注意

---

## 12. 禁止事項・注意事項

- `form/` フォルダは編集しない
- `data.json`（ルート）は削除しない（旧バージョン互換）
- `innerHTML` に未エスケープの文字列を渡さない
- `--text` カラーをリンク色としてそのまま使わない（視認性確保のため `--accent` を使う）
- Google Fonts の読み込みを削除・変更しない（全ページで同じフォントを使用）
- Leaflet を shops.html 以外のページに追加しない（不要な重さを避ける）
