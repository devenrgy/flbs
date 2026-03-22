import base64
import os
import re
import shutil
import subprocess
import tempfile
import zipfile

from config import FLIBUSTA_PATH, SAVE_PATH
from db import BookRow
from fmt import author_for_filename, make_filename, sanitize


def extract(entry: BookRow) -> None:
    os.makedirs(SAVE_PATH, exist_ok=True)
    filename = entry["FILENAME"]
    fileid   = entry["FILEID"]
    out_path = os.path.join(SAVE_PATH, make_filename(entry))
    archive  = os.path.join(FLIBUSTA_PATH, filename)

    print(f"  Extracting {fileid}.fb2 from {filename} ...")
    result = subprocess.run(
        ["7z", "-aoa", "x", archive, "-so", f"{fileid}.fb2"],
        capture_output=True,
    )
    if result.returncode != 0:
        print(f"  7z error: {result.stderr.decode(errors='replace')}")
        return

    raw_fb2  = result.stdout
    xl       = subprocess.run(["xmllint", "--format", "-"], input=raw_fb2, capture_output=True)
    fb2_text = xl.stdout if xl.returncode == 0 else raw_fb2

    zip_name   = re.sub(r"\.7z$", ".zip", filename)
    binary_xml = _collect_binaries(fileid, zip_name)

    fb2_text = fb2_text.replace(b"</FictionBook>", b"")
    with open(out_path, "wb") as f:
        f.write(fb2_text + binary_xml + b"</FictionBook>\n")
    print(f"  Saved: {out_path}")


def _collect_binaries(fileid: str, zip_name: str) -> bytes:
    binary_xml = b""
    for subfolder in ("covers", "images"):
        src_zip = os.path.join(FLIBUSTA_PATH, subfolder, zip_name)
        if not os.path.exists(src_zip):
            continue
        print(f"  Extracting {subfolder} from {zip_name} ...")
        tmp_dir = os.path.join(tempfile.gettempdir(), f"flbs_{fileid}_{subfolder}")
        os.makedirs(tmp_dir, exist_ok=True)
        try:
            with zipfile.ZipFile(src_zip, "r") as z:
                if subfolder == "covers":
                    members = [m for m in z.namelist() if m == fileid]
                else:
                    members = [m for m in z.namelist() if m.startswith(f"{fileid}/")]
                z.extractall(tmp_dir, members)
        except Exception as e:
            print(f"  Failed to unzip {subfolder}: {e}")
            shutil.rmtree(tmp_dir, ignore_errors=True)
            continue

        file_list = _collect_files(tmp_dir, fileid, subfolder)
        binary_xml += _encode_images(file_list, is_cover=(subfolder == "covers"))
        shutil.rmtree(tmp_dir, ignore_errors=True)

    return binary_xml


def _collect_files(tmp_dir: str, fileid: str, subfolder: str) -> list[str]:
    if subfolder == "covers":
        cover_path = os.path.join(tmp_dir, fileid)
        return [cover_path] if os.path.isfile(cover_path) else []
    img_dir = os.path.join(tmp_dir, fileid)
    if os.path.isdir(img_dir):
        return [os.path.join(img_dir, f) for f in sorted(os.listdir(img_dir))]
    return []


def _encode_images(file_list: list[str], *, is_cover: bool) -> bytes:
    lines: list[str] = []
    for idx, img_path in enumerate(file_list):
        orig_name = os.path.basename(img_path)
        jpeg_path = img_path + ".jpeg"
        subprocess.run(
            ["djxl", img_path, jpeg_path, "--quiet", "--output_format", "jpeg"],
            capture_output=True,
        )
        if not os.path.exists(jpeg_path):
            continue
        with open(jpeg_path, "rb") as fh:
            b64 = base64.b64encode(fh.read()).decode()
        binary_id = "cover" if (is_cover and idx == 0) else orig_name
        lines.append(f' <binary id="{binary_id}" content-type="image/jpeg">{b64}</binary>')

    if lines:
        return ("\n".join(lines) + "\n").encode()
    return b""
