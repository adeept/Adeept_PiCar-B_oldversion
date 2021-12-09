import io
import sys
import traceback

from robot.models import Config

import cv2
if sys.platform != "darwin":  # Mac OS
    import picamera


class CaptureDevice(object):

    def __init__(self, resolution, framerate, capturing_device):
        self.capturing_device = capturing_device
        self.framerate = framerate
        if self.capturing_device == "usb":  # USB Camera?
            self.device = cv2.VideoCapture(0)
            #self.device.set(cv2.CAP_PROP_FPS, framerate)
            res_x, res_y = resolution.split('x')
            self.device.set(3, float(res_x))
            self.device.set(4, float(res_y))
        else:
            self.device = picamera.PiCamera(resolution=resolution, framerate=framerate)

    def capture_continuous(self, stream, format='jpeg'):
        if self.capturing_device == "usb":
            while (True):
                ret, frame = self.device.read()
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

                yield cv2.imencode('.jpg', rgb)[1].tostring()
                if cv2.waitKey(1000 // self.framerate) & 0xFF == ord('q'):
                    break
        else:
            for frame in self.device.capture_continuous(stream,
                                                        format=format,
                                                        use_video_port=True):
                yield frame.getvalue()

    def close(self):
        if self.capturing_device == "usb":
            self.device.release()
        else:
            self.device.close()


class Camera(object):
    pwm = None
    position = {}
    streaming = False
    x_max = 0
    x_mid = 0
    x_min = 0
    y_max = 0
    y_mid = 0
    y_min = 0

    @staticmethod
    def setup(pwm):
        Camera.pwm = pwm
        Camera.ahead()

    @staticmethod
    def ahead():
        Camera.set_position(0.0, 0.0)

    @staticmethod
    def set_position(x, y):
        config = Config.get_config()
        Camera._set_x(config, x)
        Camera._set_y(config, y)

    @staticmethod
    def _set_x(config, pos):
        center_x = int(config.get('camera_center_x', 420))
        max_x = int(config.get('camera_max_x', 720))
        min_x = int(config.get('camera_min_x', 120))

        course_x = max(max_x - center_x, center_x - min_x)
        pos_x = int(center_x + pos * (course_x / 90.0))
        x = max(min(pos_x, max_x), min_x)
        Camera.position['x'] = pos
        Camera.pwm.set_pwm(1, 0, x)

    @staticmethod
    def _set_y(config, pos):
        center_y = int(config.get('camera_center_y', 340))
        max_y = int(config.get('camera_max_y', 550))
        min_y = int(config.get('camera_min_y', 270))

        course_y = max(max_y - center_y, center_y - min_y)
        pos_y = int(center_y + pos * (course_y / 90.0))
        y = max(min(pos_y, max_y), min_y)
        Camera.position['y'] = pos
        Camera.pwm.set_pwm(0, 0, y)

    @staticmethod
    def stream():
        config = Config.get_config()
        if sys.platform == "darwin":
            capturing_device = "usb"
            resolution = '1280x720'
        else:
            capturing_device = config.get('capturing_device', 'picamera')
            resolution = config.get('capturing_resolution', '1280x720')
        capture_device = CaptureDevice(resolution=resolution,
                                       framerate=int(config.get('capturing_framerate', 7)),
                                       capturing_device=capturing_device)
        stream = io.BytesIO()
        try:
            Camera.streaming = True
            for frame in capture_device.capture_continuous(stream, format='jpeg'):
                stream.truncate()
                stream.seek(0)
                yield "--FRAME\r\n"
                yield "Content-Type: image/jpeg\r\n"
                yield "Content-Length: %i\r\n" % len(frame)
                yield "\r\n"
                yield frame
                yield "\r\n"
        except Exception as e:
            traceback.print_exc()
        finally:
            capture_device.close()
            Camera.streaming = False

    @staticmethod
    def serialize():
        return {
            'position': Camera.position,
            'streaming': Camera.streaming
        }
