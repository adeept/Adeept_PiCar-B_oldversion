import io
import sys
import traceback

if sys.platform == "darwin":  # Mac OS
    import cv2
else:
    import picamera


class CaptureDevice(object):

    def __init__(self, resolution, framerate):
        if sys.platform == "darwin":  # Mac OS
            self.device = cv2.VideoCapture(0)
            self.device.set(cv2.CAP_PROP_FPS, framerate)
            res_x, res_y = resolution.split('x')
            self.device.set(3, float(res_x))
            self.device.set(4, float(res_y))
        else:
            self.device = picamera.PiCamera(resolution=resolution, framerate=framerate)

    def capture_continuous(self, stream, format='jpeg'):
        if sys.platform == "darwin":  # Mac OS
            while (True):
                ret, frame = self.device.read()
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

                yield cv2.imencode('.jpg', rgb)[1].tostring()
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        else:
            for frame in self.device.capture_continuous(stream,
                                                        format=format,
                                                        use_video_port=True):
                yield frame.getvalue()

    def close(self):
        if sys.platform == "darwin":  # Mac OS
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
    def setup(config, pwm):
        Camera.pwm = pwm
        Camera.x_max = config.get('x_max', 720)
        Camera.x_mid = config.get('x_mid', 420)
        Camera.x_min = config.get('x_min', 120)
        Camera.y_max = config.get('y_max', 550)
        Camera.y_mid = config.get('y_mid', 340)
        Camera.y_min = config.get('y_min', 270)
        Camera.ahead()

    @staticmethod
    def ahead():
        Camera.set_position(0.0, 0.0)

    @staticmethod
    def set_position(x, y):
        Camera._set_x(x)
        Camera._set_y(y)

    @staticmethod
    def _set_x(pos):
        course_x = Camera.x_max - Camera.x_mid
        pos_x = int(Camera.x_mid + pos * (course_x / 90.0))
        x = max(min(pos_x, Camera.x_max), Camera.x_min)
        Camera.position['x'] = pos
        Camera.pwm.set_pwm(1, 0, x)

    @staticmethod
    def _set_y(pos):
        course_y = Camera.y_max - Camera.y_mid
        pos_y = int(Camera.y_mid + pos * (course_y / 90.0))
        y = max(min(pos_y, Camera.y_max), Camera.y_min)
        Camera.position['y'] = pos
        Camera.pwm.set_pwm(0, 0, y)

    @staticmethod
    def stream():
        capture_device = CaptureDevice(resolution='640x480', framerate=7)
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
