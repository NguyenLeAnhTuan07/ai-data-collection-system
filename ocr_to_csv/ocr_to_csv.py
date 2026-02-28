import os
import csv
from PIL import Image
import pytesseract
from tqdm import tqdm

# ================== CONFIG ==================

# BẮT BUỘC GIỮ DÒNG NÀY
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

IMAGE_DIR = "loc"          # thư mục chứa ảnh
OUTPUT_CSV = "dataset_text.csv"  # file output
LABEL = 0                         # 0 = sạch, 1 = phishing (đổi tại đây)

VALID_EXT = (".png", ".jpg", ".jpeg", ".bmp", ".tiff")

# ================== OCR FUNCTION ==================

def ocr_image(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(
            img,
            lang="eng+vie",
            config="--psm 6"
        )
        text = text.strip().replace("\n", " ")
        return text
    except Exception as e:
        print(f"Error OCR {image_path}: {e}")
        return ""

# ================== MAIN ==================

def main():
    images = [
        f for f in os.listdir(IMAGE_DIR)
        if f.lower().endswith(VALID_EXT)
    ]

    print(f"Found {len(images)} images")

    total_lines = 0

    with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)

        for img_name in tqdm(images):
            img_path = os.path.join(IMAGE_DIR, img_name)
            text = ocr_image(img_path)

            if text.strip():
                writer.writerow([LABEL, text])
                total_lines += 1

    print("\nDONE!")
    print(f"Saved to {OUTPUT_CSV}")
    print(f"Total lines: {total_lines}")

# ================== RUN ==================

if __name__ == "__main__":
    main()
