
class Steering:
    PWM = None
    HeadingMax = 0
    HeadingMin = 0

    @staticmethod
    def setup(config, pwm):
        Steering.PWM = pwm
        Steering.HeadingMin = config.get('heading_min', 300)
        Steering.HeadingMax = config.get('heading_max', 500)
        Steering.middle()

    @staticmethod
    def head(heading):
        course = Steering.HeadingMax - Steering.HeadingMin
        value = int(Steering.HeadingMin + (heading + 90.0) * (course / 180.0))
        Steering.PWM.set_pwm(2, 0, value)

    @staticmethod
    def middle():
        Steering.PWM.set_pwm(2, 0, int((Steering.HeadingMax + Steering.HeadingMin) / 2))
