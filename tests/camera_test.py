import time
import picamera

import warnings
warnings.filterwarnings('error', category=DeprecationWarning)

with picamera.PiCamera() as camera:
    camera.resolution = (480, 360)
    # camera.framerate = (24, 1)
    camera.start_preview()
    # camera.preview_fullscreen = True
    # camera.preview_alpha = 128
    time.sleep(10)
    # camera.raw_format = 'yuv'
    # stream = io.BytesIO()
    # camera.capture(stream, 'raw', use_video_port=True)
    camera.stop_preview()