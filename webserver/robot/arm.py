from robot.models import Config


class Arm:
    PWM = None

    @staticmethod
    def setup(pwm):
        Arm.PWM = pwm
        Arm.down()

    @staticmethod
    def move_elbow(angle):
        config = Config.get_config()
        up = int(config.get('elbow_up', 400))
        down = int(config.get('elbow_down', 665))
        course = down - up
        value = int(up + (90.0 - angle) * (course / 90.0))
        Arm.PWM.set_pwm(3, 0, value)

    @staticmethod
    def move_claw(angle):
        config = Config.get_config()
        close_pos = int(config.get('claw_close', 600))
        open_pos = int(config.get('claw_open', 300))
        course = close_pos - open_pos
        value = int(open_pos + (90.0 - angle) * (course / 90.0))
        Arm.PWM.set_pwm(4, 0, value)

    @staticmethod
    def down():
        Arm.move_elbow(0)
        Arm.move_claw(0)
