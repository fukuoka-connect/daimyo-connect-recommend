#!/usr/bin/env python3
"""
Google Places API (New) で全店舗の正確な座標を取得して shops.json を更新するスクリプト。

使い方:
  GOOGLE_API_KEY=xxx python3 scripts/geocode_with_google.py
  GOOGLE_API_KEY=xxx python3 scripts/geocode_with_google.py --dry-run  # 反映せず確認のみ
  GOOGLE_API_KEY=xxx python3 scripts/geocode_with_google.py --only-dup  # 重複座標店だけ
"""
import json, os, sys, time, urllib.parse, urllib.request, math
from collections import Counter

API_KEY = os.environ.get("GOOGLE_API_KEY")
if not API_KEY:
    print("ERROR: 環境変数 GOOGLE_API_KEY を設定してください")
    print("例: GOOGLE_API_KEY=AIza... python3 scripts/geocode_with_google.py")
    sys.exit(1)

DRY_RUN = "--dry-run" in sys.argv
ONLY_DUP = "--only-dup" in sys.argv

# cid付きの既確定店はスキップ
CID_CONFIRMED = {"oneday","skb-koji","mint-bar-hacca","com-stand","komatakaman","pinon-bar",
            "place-of-all-rush","koubashiya","shokudou-owan","bruntjet","ponta","loulou",
            "sofuren-umi","green-beach-house"}

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOPS_FILE = os.path.join(ROOT, "data", "shops.json")

def hav(a,b,c,d):
    R=6371000
    la1,la2=math.radians(a),math.radians(c)
    dla,dlo=math.radians(c-a),math.radians(d-b)
    x=math.sin(dla/2)**2+math.cos(la1)*math.cos(la2)*math.sin(dlo/2)**2
    return 2*R*math.asin(math.sqrt(x))

def places_search(name, address):
    """Places API (New) Text Search で店舗を検索して位置を取得"""
    url = "https://places.googleapis.com/v1/places:searchText"
    body = {
        "textQuery": f"{name} {address}",
        "languageCode": "ja",
        "regionCode": "JP",
        "maxResultCount": 1,
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode(),
        headers={
            "Content-Type": "application/json",
            "X-Goog-Api-Key": API_KEY,
            "X-Goog-FieldMask": "places.location,places.displayName,places.formattedAddress,places.id",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read())
        if "places" in data and data["places"]:
            p = data["places"][0]
            loc = p.get("location", {})
            return {
                "lat": loc.get("latitude"),
                "lng": loc.get("longitude"),
                "name": p.get("displayName", {}).get("text", ""),
                "address": p.get("formattedAddress", ""),
                "place_id": p.get("id", ""),
            }
    except Exception as e:
        print(f"  ERR: {e}")
    return None

def main():
    with open(SHOPS_FILE) as f:
        data = json.load(f)
    shops = data["shops"]

    # 重複座標検出
    coord_count = Counter()
    for s in shops:
        c = s.get("coordinates") or {}
        if c.get("lat"):
            coord_count[(round(c["lat"],4), round(c["lng"],4))] += 1

    targets = []
    for s in shops:
        if s["id"] in CID_CONFIRMED:
            continue
        c = s.get("coordinates") or {}
        is_dup = c.get("lat") and coord_count[(round(c["lat"],4), round(c["lng"],4))] > 1
        if ONLY_DUP and not is_dup:
            continue
        targets.append(s)

    print(f"対象: {len(targets)}店舗 (DRY_RUN={DRY_RUN})")
    print(f"推定API呼び出し: {len(targets)}回 / 想定コスト: ${len(targets)*0.017:.2f}（無料枠内）\n")

    updates = []
    for i, s in enumerate(targets, 1):
        print(f"[{i}/{len(targets)}] {s['name']} ({s['area']})")
        r = places_search(s["name"], s.get("address",""))
        time.sleep(0.2)
        if not r or not r["lat"]:
            print(f"  → 取得失敗")
            continue
        cur = s.get("coordinates") or {}
        if cur.get("lat"):
            d = hav(cur["lat"], cur["lng"], r["lat"], r["lng"])
        else:
            d = 99999
        print(f"  → {r['lat']:.7f}, {r['lng']:.7f}  (移動{d:.0f}m) [{r['name']}]")
        updates.append((s, r, d))
        if not DRY_RUN:
            s["coordinates"] = {"lat": r["lat"], "lng": r["lng"]}
            if not s.get("googleMapUrl") and r.get("place_id"):
                s["googleMapUrl"] = f"https://www.google.com/maps/place/?q=place_id:{r['place_id']}"

    if not DRY_RUN:
        with open(SHOPS_FILE, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n✓ {len(updates)}店舗を更新 → {SHOPS_FILE}")
    else:
        print(f"\n[DRY RUN] 更新対象: {len(updates)}店舗（実際の書き込みなし）")

if __name__ == "__main__":
    main()
