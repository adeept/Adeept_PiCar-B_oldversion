from robot.models import Config


class Arm:
    PWM = None

    @staticmethod
    def setup(pwm):
        Arm.PWM = pwm
        Arm.down()

    @staticmethod
    def lift_elbow(angle):
        config = Config.get_config()
        up = int(config.get('elbow_up', 400))
        down = int(config.get('elbow_down', 600))
        course = down - up
        value = int(up + angle * (course / 90.0))
        Arm.PWM.set_pwm(3, 0, value)

    @staticmethod
    def down():
        Arm.lift_elbow(0)
