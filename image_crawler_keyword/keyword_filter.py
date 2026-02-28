import os
import shutil
from PIL import Image
import imagehash

# ================= CONFIG =================

SOURCE_DIR = "dataset"
MERGED_DIR = "tonghopanh"
FINAL_DIR = "filter"

IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".bmp", ".webp")
HASH_THRESHOLD = 5   # cho phép gần trùng

# ==========================================

os.makedirs(MERGED_DIR, exist_ok=True)
os.makedirs(FINAL_DIR, exist_ok=True)

# =========================================================
# PHASE 1: MERGE
# =========================================================

print("=== PHASE 1: MERGING ===")
merge_count = 0

for root, dirs, files in os.walk(SOURCE_DIR):
    for file in files:
        if not file.lower().endswith(IMAGE_EXTS):
            continue

        src_path = os.path.join(root, file)
        parent_folder = os.path.basename(root)
        new_name = f"{parent_folder}_{file}"
        dest_path = os.path.join(MERGED_DIR, new_name)

        shutil.copy2(src_path, dest_path)
        merge_count += 1

print(f"Merged images: {merge_count}")
print("Merge done.\n")

# =========================================================
# PHASE 2: BK-TREE FOR DEDUPLICATION
# =========================================================

print("=== PHASE 2: FILTERING (BK-TREE) ===")

class BKTree:
    def __init__(self, dist_func):
        self.dist_func = dist_func
        self.tree = None

    def add(self, item):
        if self.tree is None:
            self.tree = (item, {})
            return

        node = self.tree
        while True:
            node_item, children = node
            d = self.dist_func(item, node_item)

            if d in children:
                node = children[d]
            else:
                children[d] = (item, {})
                break

    def search(self, item, threshold):
        if self.tree is None:
            return []

        candidates = [self.tree]
        results = []

        while candidates:
            node_item, children = candidates.pop()
            d = self.dist_func(item, node_item)

            if d <= threshold:
                results.append(node_item)

            for dist in range(d - threshold, d + threshold + 1):
                child = children.get(dist)
                if child:
                    candidates.append(child)

        return results


def hamming_distance(h1, h2):
    return abs(h1 - h2)


bk_tree = BKTree(hamming_distance)

count_keep = 0
count_skip = 0

for file in os.listdir(MERGED_DIR):

    if not file.lower().endswith(IMAGE_EXTS):
        continue

    img_path = os.path.join(MERGED_DIR, file)

    try:
        img = Image.open(img_path).convert("RGB")
        h = imagehash.average_hash(img)

        matches = bk_tree.search(h, HASH_THRESHOLD)

        if matches:
            count_skip += 1
            continue

        bk_tree.add(h)

        new_name = f"img_{count_keep}.jpg"
        shutil.copy2(img_path, os.path.join(FINAL_DIR, new_name))
        count_keep += 1

    except Exception as e:
        print("Error:", img_path, e)

print("\nDONE")
print("Kept images:", count_keep)
print("Skipped duplicates:", count_skip)
print("Final images stored in:", FINAL_DIR)