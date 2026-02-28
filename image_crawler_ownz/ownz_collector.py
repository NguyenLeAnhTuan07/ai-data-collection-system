from playwright.sync_api import sync_playwright
import time
import os
import re
from urllib.parse import urlparse
from multiprocessing import Process, current_process


def start_browser():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page(
        viewport={"width": 1920, "height": 1080},
        ignore_https_errors=True
    )
    return playwright, browser, page

def open_report(page, report_url):
    page.goto(report_url, timeout=60000)
    page.wait_for_load_state("networkidle")
    time.sleep(1)

def capture_hacked_image(page, save_path):
    iframe = page.locator("iframe[src*='mirror']")
    if iframe.count() > 0:
        iframe.first.screenshot(path=save_path)
    else:
        page.screenshot(path=save_path, full_page=True)


def extract_web_url(page):
    try:
        header_text = page.locator("text=Web URL").first.locator("..").inner_text()
    except:
        header_text = page.inner_text("body")

    match = re.search(r'https?://[^\s"]+', header_text)
    if not match:
        return None

    web_url = match.group(0).strip()
    parsed = urlparse(web_url)

    if not parsed.scheme or not parsed.netloc:
        return None

    return web_url


def capture_fixed_image(page, web_url, save_path):
    page.goto(web_url, timeout=60000)
    page.wait_for_load_state("networkidle")
    time.sleep(2)
    page.screenshot(path=save_path, full_page=True)


def worker(zone_ids):
    name = current_process().name
    print(f"[+] {name} started ({len(zone_ids)} zones)")

    playwright, browser, page = start_browser()

    try:
        for zone_id in zone_ids:
            hacked_path = f"dataset/hacked/{zone_id}.png"
            fixed_path  = f"dataset/fixed/{zone_id}.png"

            if os.path.exists(hacked_path) and os.path.exists(fixed_path):
                print(f"[{name}] Skip {zone_id}")
                continue

            report_url = f"https://ownzyou.com/zone/{zone_id}"
            print(f"[{name}] ZONE {zone_id}")

            try:
                open_report(page, report_url)
                capture_hacked_image(page, hacked_path)

                web_url = extract_web_url(page)
                if not web_url:
                    print(f"[{name}] No Web URL {zone_id}")
                    continue

                capture_fixed_image(page, web_url, fixed_path)

                with open("dataset/log.csv", "a", encoding="utf-8") as f:
                    f.write(f"{zone_id},{web_url}\n")

                time.sleep(1)

            except Exception as e:
                print(f"[{name}] Error {zone_id}: {e}")

    finally:
        browser.close()
        playwright.stop()
        print(f"[✓] {name} finished")

def main():
    start_id = int(input("👉 Nhập START ID (vd 276117): "))
    count = int(input("👉 Nhập SỐ LƯỢNG muốn crawl: "))
    workers = int(input("👉 Nhập SỐ WORKER (vd 10): "))

    end_id = start_id - count + 1
    zone_ids = list(range(start_id, end_id - 1, -1))

    os.makedirs("dataset/hacked", exist_ok=True)
    os.makedirs("dataset/fixed", exist_ok=True)

    buckets = [[] for _ in range(workers)]
    for i, zid in enumerate(zone_ids):
        buckets[i % workers].append(zid)

    processes = []
    for i in range(workers):
        p = Process(
            target=worker,
            args=(buckets[i],),
            name=f"Worker-{i+1}"
        )
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    print("\n[✓] ALL DONE")
def merge_dataset():
    hacked_dir = "dataset/hacked"
    fixed_dir = "dataset/fixed"

    out_hacked = "dataset/merged/hacked"
    out_fixed  = "dataset/merged/fixed"

    os.makedirs(out_hacked, exist_ok=True)
    os.makedirs(out_fixed, exist_ok=True)

    hacked_files = set(os.listdir(hacked_dir))
    fixed_files  = set(os.listdir(fixed_dir))

    common_ids = sorted(
        f.replace(".png", "")
        for f in hacked_files
        if f in fixed_files
    )

    print(f"[+] Found {len(common_ids)} paired samples")

    with open("dataset/merged/pairs.csv", "w", encoding="utf-8") as f:
        f.write("pair_id,hacked,fixed,zone_id\n")

        for idx, zone_id in enumerate(common_ids, start=1):
            pair_id = f"{idx:06d}"

            src_hacked = os.path.join(hacked_dir, f"{zone_id}.png")
            src_fixed  = os.path.join(fixed_dir, f"{zone_id}.png")

            dst_hacked = os.path.join(out_hacked, f"{pair_id}.png")
            dst_fixed  = os.path.join(out_fixed,  f"{pair_id}.png")

            if not os.path.exists(dst_hacked):
                with open(src_hacked, "rb") as s, open(dst_hacked, "wb") as d:
                    d.write(s.read())

            if not os.path.exists(dst_fixed):
                with open(src_fixed, "rb") as s, open(dst_fixed, "wb") as d:
                    d.write(s.read())

            f.write(f"{pair_id},{dst_hacked},{dst_fixed},{zone_id}\n")

    print("[✓] Dataset merged successfully")

if __name__== "__main__":
    main()
    merge_dataset()