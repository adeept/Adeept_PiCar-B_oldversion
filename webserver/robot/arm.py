from robot.models import Config


class Arm:
    PWM = None
    elbow_angle = 90
    claw_angle = 90

    @staticmethod
    def setup(pwm):
        Arm.PWM = pwm
        Arm.park()

    @staticmethod
    def move_elbow(angle):
        Arm.arm_angle = angle
        config = Config.get_config()
        up = int(config.get('elbow_up', 400))
        down = int(config.get('elbow_down', 665))
        course = down - up
        value = int(up + (90.0 - angle) * (course / 90.0))
        Arm.PWM.set_pwm(3, 0, value)

    @staticmethod
    def move_claw(angle):
        Arm.claw_angle = angle
        config = Config.get_config()
        close_pos = int(config.get('claw_close', 600))
        open_pos = int(config.get('claw_open', 300))
        course = close_pos - open_pos
        value = int(open_pos + (90.0 - angle) * (course / 90.0))
        Arm.PWM.set_pwm(4, 0, value)

    @staticmethod
    def park():
        Arm.move_elbow(90)
        Arm.move_claw(90)

    @staticmethod
    def serialize():
        return {
            'elbow_angle': Arm.elbow_angle,
            'claw_angle': Arm.claw_angle
        }
