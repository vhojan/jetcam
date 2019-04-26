from .camera import Camera
import atexit
import cv2
import numpy as np
import threading
import traitlets


class IMX219(Camera):
    
    capture_fps = traitlets.Integer(default_value=21)
    capture_width = traitlets.Integer(default_value=3280)
    capture_height = traitlets.Integer(default_value=2464)

    def __init__(self, *args, **kwargs):
        super(IMX219, self).__init__(*args, **kwargs)
        try:
            self.cap = cv2.VideoCapture(self._gst_str(), cv2.CAP_GSTREAMER)

            re, image = self.cap.read()

            if not re:
                raise RuntimeError('Could not read image from camera.')
        except:
            raise RuntimeError(
                'Could not initialize camera.  Please see error trace.')

        atexit.register(self.cap.release)
                
    def _gst_str(self):
        return 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=%d, height=%d, format=(string)NV12, framerate=(fraction)%d/1 ! nvvidconv ! video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! videoconvert ! appsink' % (
                self.capture_width, self.capture_height, self.capture_fps, self.width, self.height)
    
    def _read(self):
        re, image = self.cap.read()
        if re:
            return image
        else:
            raise RuntimeError('Could not read image from camera')