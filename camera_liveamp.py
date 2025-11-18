import time
from pathlib import Path

import mss
from mss import tools

# Folder where screenshots will be stored
SAVE_DIR = Path("Development/frames")
SAVE_DIR.mkdir(parents=True, exist_ok=True)


def main():
    with mss.mss() as sct:
        # Monitor 1 = primary display. If you have multiple, adjust index.
        monitor = sct.monitors[1]

        while True:
            ts = int(time.time() * 1000)
            path = SAVE_DIR / f"screen_{ts}.png"

            # Grab full-screen
            sct_img = sct.grab(monitor)

            # Save as PNG
            tools.to_png(sct_img.rgb, sct_img.size, output=str(path))
            print(f"Saved {path}")

            # Adjust capture rate (0.5s = 2 fps)
            time.sleep(10)


if __name__ == "__main__":
    main()

