from mss import mss
from pathlib import Path
from PIL import Image
import time

SAVE_DIR = Path("screenshots")
SAVE_DIR.mkdir(exist_ok=True)

def main():
    with mss() as sct:
        monitor = sct.monitors[1]  # 1 = primary monitor

        while True:
            sct_img = sct.grab(monitor)

            # Convert MSS raw data → Pillow image
            img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)

            ts = int(time.time() * 1000)
            out_path = SAVE_DIR / f"screen_{ts}.jpg"

            # Save as JPEG instead of PNG
            img.save(out_path, "JPEG", quality=80)
            print("Saved", out_path)

            time.sleep(5)  # every 5 seconds

if __name__ == "__main__":
    main()

