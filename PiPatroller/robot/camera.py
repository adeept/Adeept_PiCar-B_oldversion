import io
import traceback

import picamera


class Camera:
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
        Camera.x_max = config.get('x_max', 500)
        Camera.x_mid = config.get('x_mid', 300)
        Camera.x_min = config.get('x_min', 100)
        Camera.y_max = config.get('y_max', 570)
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
        camera = picamera.PiCamera(resolution='640x480', framerate=7)
        stream = io.BytesIO()
        try:
            Camera.streaming = True
            for frame in camera.capture_continuous(stream,
                                                   format='jpeg',
                                                   use_video_port=True):
                stream.truncate()
                stream.seek(0)
                yield "--FRAME\r\n"
                yield "Content-Type: image/jpeg\r\n"
                yield "Content-Length: %i\r\n" % len(frame.getvalue())
                yield "\r\n"
                yield frame.getvalue()
                yield "\r\n"
        except Exception as e:
            traceback.print_exc()
        finally:
            camera.close()
            Camera.streaming = False

    @staticmethod
    def serialize():
        return {
            'position': Camera.position,
            'streaming': Camera.streaming
        }
