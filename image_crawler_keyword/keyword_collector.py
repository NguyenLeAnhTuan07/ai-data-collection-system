import os
import requests
import time
from io import BytesIO
from ddgs import DDGS
from PIL import Image
import imagehash

# ================= CONFIG =================
SAVE_DIR = "dataset"
MAX_IMAGES_PER_KEYWORD = 25
DELAY_BETWEEN_DOWNLOAD = 2

KEYWORDS = [
    "legitimate business email screenshot",
    "official bank email screenshot"

]

suffixes = ["screenshot", "document"]

# ===========================================

os.makedirs(SAVE_DIR, exist_ok=True)
downloaded_hashes = set()

# ===== SEARCH FUNCTION (ANTI RATE LIMIT) =====
def search_images(keyword, max_images=30):
    for _ in range(3):  # thử 3 lần
        try:
            with DDGS() as ddgs:
                return list(ddgs.images(keyword, max_results=max_images))
        except Exception as e:
            print("Rate limited... waiting 10s", e)
            time.sleep(10)
    return []

# ===== CHECK DUPLICATE =====
def is_duplicate(img_bytes):
    try:
        img = Image.open(BytesIO(img_bytes))
        h = imagehash.average_hash(img)
        if h in downloaded_hashes:
            return True
        downloaded_hashes.add(h)
        return False
    except:
        return True

# ===== DOWNLOAD =====
def download_images(keyword, max_images=30):
    print(f"\nSearching: {keyword}")
    folder = os.path.join(SAVE_DIR, keyword.replace(" ", "_"))
    os.makedirs(folder, exist_ok=True)

    results = search_images(keyword, max_images)

    for i, r in enumerate(results):
        try:
            img_url = r["image"]
            response = requests.get(img_url, timeout=8)
            img_bytes = response.content

            if len(img_bytes) > 3_000_000:
                continue

            if is_duplicate(img_bytes):
                print("Duplicate skipped")
                continue

            filename = f"{keyword.replace(' ', '_')}_{i}.jpg"
            path = os.path.join(folder, filename)

            with open(path, "wb") as f:
                f.write(img_bytes)

            print("Saved:", filename)
            time.sleep(DELAY_BETWEEN_DOWNLOAD)

        except Exception as e:
            print("Error:", e)

# ===== MAIN LOOP =====
for kw in KEYWORDS:
    download_images(kw, MAX_IMAGES_PER_KEYWORD)

    for s in suffixes:
        new_kw = kw + " " + s
        download_images(new_kw, MAX_IMAGES_PER_KEYWORD)

print("\nDONE !!!")
