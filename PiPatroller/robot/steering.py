from robot.models import Config


class Steering:
    PWM = None

    @staticmethod
    def setup(pwm):
        Steering.PWM = pwm
        Steering.middle()

    @staticmethod
    def head(heading):
        config = Config.get_config()
        course = int(config.get('steering_course', 200))
        center = int(config.get('steering_center', 400))
        head_min = int(center - course/2)
        value = int(head_min + (heading + 90.0) * (course / 180.0))
        Steering.PWM.set_pwm(2, 0, value)

    @staticmethod
    def middle():
        Steering.head(0)
