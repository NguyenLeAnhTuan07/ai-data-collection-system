import os
from PIL import Image
import imagehash
from tqdm import tqdm
import csv

RAW_HACKED = "dataset/hacked"
RAW_FIXED  = "dataset/fixed"

OUT_HACKED = "filter/hacked"
OUT_FIXED  = "filter/fixed"
OUT_CSV    = "filter/pairs.csv"

os.makedirs(OUT_HACKED, exist_ok=True)
os.makedirs(OUT_FIXED, exist_ok=True)

THRESHOLD = 8

hashes = []
kept = []  # lưu filename gốc đã được lọc

print("[+] Deduplicating dataset (safe mode)...")

for img_name in tqdm(sorted(os.listdir(RAW_HACKED))):
    hacked_path = os.path.join(RAW_HACKED, img_name)
    fixed_path  = os.path.join(RAW_FIXED, img_name)

    if not os.path.exists(fixed_path):
        continue

    try:
        img = Image.open(hacked_path).convert("RGB")
        ph = imagehash.phash(img)

        if any(abs(ph - h) <= THRESHOLD for h in hashes):
            continue

        hashes.append(ph)
        kept.append(img_name)

        pair_id = f"{len(kept):06d}"
        zone_id = img_name.replace(".png", "")

        img.save(os.path.join(OUT_HACKED, f"{pair_id}.png"))
        Image.open(fixed_path).save(os.path.join(OUT_FIXED, f"{pair_id}.png"))

    except Exception as e:
        print("Error:", img_name, e)

print(f"[✓] Unique images added: {len(kept)}")


# ghi pairs.csv (append)

csv_exists = os.path.exists(OUT_CSV)

with open(OUT_CSV, "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    if not csv_exists:
        writer.writerow(["pair_id", "hacked", "fixed", "zone_id"])

    start_idx = sum(1 for _ in open(OUT_CSV, encoding="utf-8")) - 1

    for i, fname in enumerate(kept, start=1):
        pair_id = f"{start_idx + i:06d}"
        zone_id = fname.replace(".png", "")

        writer.writerow([
            pair_id,
            f"hacked/{pair_id}.png",
            f"fixed/{pair_id}.png",
            zone_id
        ])


# XOÁ CHỈ ẢNH ĐÃ LỌC

for fname in kept:
    hp = os.path.join(RAW_HACKED, fname)
    fp = os.path.join(RAW_FIXED, fname)

    if os.path.exists(hp):
        os.remove(hp)
    if os.path.exists(fp):
        os.remove(fp)

print("[✓] Raw crawl cleaned (only processed images removed)")