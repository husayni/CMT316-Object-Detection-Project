#!/usr/bin/env python3
import os
import sys
import tarfile
import urllib.request
from urllib.error import URLError, HTTPError

def download_file(url: str, dest_path: str, chunk_size: int = 8192) -> None:
    """
    Download a file from `url` to `dest_path`, showing a simple progress indicator.
    Skips download if file already exists.
    """
    if os.path.exists(dest_path):
        print(f"[SKIP] '{dest_path}' already exists.")
        return

    try:
        with urllib.request.urlopen(url) as response:
            total_size = response.getheader('Content-Length')
            total_size = int(total_size) if total_size else None
            downloaded = 0

            with open(dest_path, 'wb') as out_file:
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    out_file.write(chunk)
                    downloaded += len(chunk)
                    if total_size:
                        percent = downloaded / total_size * 100
                        print(f"\rDownloading {os.path.basename(dest_path)}: {percent:5.1f}%", end="")
            print("\n[OK] Download complete.")

    except HTTPError as e:
        print(f"\n[ERROR] HTTP {e.code}: {e.reason} for {url}")
        sys.exit(1)
    except URLError as e:
        print(f"\n[ERROR] URL error: {e.reason} for {url}")
        sys.exit(1)

def extract_tar(file_path: str, extract_to: str) -> None:
    """
    Extracts `file_path` (must be a tar archive) into directory `extract_to`.
    """
    if not tarfile.is_tarfile(file_path):
        print(f"[ERROR] '{file_path}' is not a valid tar archive.")
        sys.exit(1)

    with tarfile.open(file_path, 'r') as tar:
        tar.extractall(path=extract_to)
    print(f"[OK] Extracted '{os.path.basename(file_path)}' → '{extract_to}/'")

def main():
    base_url = "http://host.robots.ox.ac.uk/pascal/VOC/voc2012"
    archives = [
        "VOCtrainval_11-May-2012.tar",  # images and annotations for train+val 2012
        # "VOCtest_06-Nov-2007.tar"       # test 2007 set (often used for legacy tests)
    ]

    download_dir = "downloads"
    extract_dir = "VOCdevkit"

    # Create target directories
    os.makedirs(download_dir, exist_ok=True)
    os.makedirs(extract_dir, exist_ok=True)

    for archive in archives:
        url = f"{base_url}/{archive}"
        dest_path = os.path.join(download_dir, archive)

        print(f"\n→ Processing '{archive}'")
        download_file(url, dest_path)
        extract_tar(dest_path, extract_dir)

    print("\nAll done! Your VOC data is in the 'VOCdevkit/' directory.")

if __name__ == "__main__":
    main()