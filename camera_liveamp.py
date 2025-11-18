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
            time.sleep(0.5)


if __name__ == "__main__":
    main()

# from flask import Flask, Response
# import cv2
# import threading
# import time
# from pathlib import Path

# app = Flask(__name__)

# # Global frame storage
# latest_frame = None
# frame_lock = threading.Lock()

# # Folder where snapshots are stored
# SAVE_DIR = Path("Development/frames")
# SAVE_DIR.mkdir(parents=True, exist_ok=True)


# def camera_thread():
#     global latest_frame

#     for backend in [cv2.CAP_V4L2, cv2.CAP_ANY]:
#         cap = cv2.VideoCapture(0, backend)

#         if not cap.isOpened():
#             cap.release()
#             continue

#         print(f"Camera opened with backend {backend}")

#         cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
#         cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#         cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

#         for _ in range(10):
#             cap.read()

#         try:
#             while True:
#                 ret, frame = cap.read()
#                 if ret:
#                     with frame_lock:
#                         latest_frame = frame.copy()
#                 else:
#                     time.sleep(0.1)
#         finally:
#             cap.release()
#         break



# @app.route('/save_snapshot')
# def save_snapshot():
#     """Save the current frame to disk and return a message."""
#     with frame_lock:
#         if latest_frame is None:
#             return "No frame yet", 503
#         frame = latest_frame.copy()

#     ts = int(time.time() * 5000)  # timestamp-based filename
#     path = SAVE_DIR / f"frame_{ts}.jpg"
#     cv2.imwrite(str(path), frame)
#     return f"Saved {path}", 200


# @app.route('/stream')
# def video_feed():
#     """Return the current frame as a single JPEG (not MJPEG)."""
#     with frame_lock:
#         if latest_frame is None:
#             return "No frame yet", 503
#         frame = latest_frame.copy()

#     ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
#     if not ret:
#         return "Encoding error", 500

#     return Response(buffer.tobytes(), mimetype='image/jpeg')


# @app.route('/')
# def index():
#     return "Livemap Running! Use /stream for current frame or /save_snapshot to save."


# if __name__ == '__main__':
#     print("Starting camera thread...")
#     thread = threading.Thread(target=camera_thread, daemon=True)
#     thread.start()
#     time.sleep(3)

#     # print("Starting server on http://10.32.244.149:5000/stream")
#     app.run(host='0.0.0.0', port=5000, threaded=True)

# from flask import Flask, Response
# import cv2
# import threading
# import time
# from pathlib import Path
# import time

# app = Flask(__name__)

# # Global frame storage
# latest_frame = None
# frame_lock = threading.Lock()
# SAVE_DIR = Path("Development/frames")
# SAVE_DIR.mkdir(exist_ok=True)

# def camera_thread():
#     global latest_frame
    
#     # Try different backends
#     for backend in [cv2.CAP_V4L2, cv2.CAP_ANY]:
#         cap = cv2.VideoCapture(0, backend)
        
#         if cap.isOpened():
#             print(f"Camera opened with backend {backend}")
            
#             # Try setting format
#             cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
#             cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#             cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            
#             # Skip first few frames
#             for _ in range(10):
#                 cap.read()
            
#             while True:
#                 ret, frame = cap.read()
#                 if ret:
#                     with frame_lock:
#                         latest_frame = frame.copy()
#                 else:
#                     time.sleep(0.1)
                    
#                 cap.release()
#                 break


# @app.route('/save_snapshot')
# def save_snapshot():
#     with frame_lock:
#         if latest_frame is None:
#             return "No frame yet", 503
#         frame = latest_frame.copy()
    
#     ts = int(time.time() * 5000)
#     path = SAVE_DIR / f"frame_{ts}.jpg"
#     cv2.imwrite(str(path), frame)
#     return f"Saved {path}", 200

# # def generate_frames():
# #         while True:
# #             with frame_lock:
# #                 if latest_frame is None:
# #                     time.sleep(0.1)
# #                     continue
# #                 frame = latest_frame.copy()
            
# #             ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
# #             if ret:
# #                 yield (b'--frame\r\n'
# #                     b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            
# #             time.sleep(0.033)

# @app.route('/stream')
# def video_feed():
#     return Response(save_snapshot(),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/')
# def index():
#     return "Livemap Running! Go to /livemap"

# if __name__ == '__main__':
#     print("Starting camera thread...")
#     thread = threading.Thread(target=camera_thread, daemon=True)
#     thread.start()
#     time.sleep(3)
    
#     # print("Starting server on http://10.32.244.149:5000/stream")
#     app.run(host='0.0.0.0', port=5000, threaded=True)

