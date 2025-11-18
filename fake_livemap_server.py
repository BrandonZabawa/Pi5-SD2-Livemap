#!/usr/bin/env python3
import argparse
import http.server
import os
import socketserver
import threading

IMAGE_DIR = None
IMAGES = []
INDEX = 0
LOCK = threading.Lock()

def load_images(directory = "C://home//bzabawa123//Development//frames"):
    global IMAGE_DIR, IMAGES, INDEX
    IMAGE_DIR = os.path.abspath(directory)
    files = sorted(
        f for f in os.listdir(IMAGE_DIR)
        if f.lower().endswith(('.jpg', '.jpeg'))
    )
    if not files:
        raise RuntimeError(f"No JPG images found in {IMAGE_DIR}")

    IMAGES = files
    INDEX = 0
    print(f"[LiveMap] Loaded {len(IMAGES)} JPG images from {IMAGE_DIR}")
    for i, name in enumerate(IMAGES):
        print(f"  [{i}] {name}")

class LiveMapHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global INDEX
        if self.path.startswith("../frame/next"):
            with LOCK:
                fname = IMAGES[INDEX]
                INDEX = (INDEX + 1) % len(IMAGES)

            fpath = os.path.join(IMAGE_DIR, fname)
            try:
                with open(fpath, "rb") as f:
                    data = f.read()
            except OSError as e:
                self.send_response(500)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(f"Error reading {fname}: {e}".encode("utf-8"))
                return

            self.send_response(200)
            self.send_header("Content-Type", "image/jpeg")
            self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
            self.end_headers()
            self.wfile.write(data)
            print(f"[LiveMap] Served {fname}")
        else:
          # simple 404
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Not found")

    def log_message(self, fmt, *args):
        # silence default logging; you already get our prints
        return

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", required=True, help="Directory with JPG frames")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    load_images(args.dir)

    with socketserver.TCPServer((args.host, args.port), LiveMapHandler) as httpd:
        print(f"[LiveMap] Server running on {args.host}:{args.port}")
        httpd.serve_forever()

if __name__ == "__main__":
    main()

