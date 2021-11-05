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
        down = int(config.get('elbow_down', 200))
        course = up - down
        value = int(down + angle * (course / 90.0))
        Arm.PWM.set_pwm(3, 0, value)

    @staticmethod
    def down():
        Arm.lift_elbow(0)
