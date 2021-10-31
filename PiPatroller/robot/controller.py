import time

import pyttsx3
from robot.camera import Camera
from robot.led import Led
from robot.models import Config
from robot.motor import Motor
from robot.steering import Steering
from robot.ultra import Ultra

from threading import Timer

try:
    import Adafruit_PCA9685
    pwm = Adafruit_PCA9685.PCA9685()
except:
    from unittest.mock import Mock
    pwm = Mock()
    pwm.set_pwm = lambda *args : print("pwm.set_pwm{}".format(args))
pwm.set_pwm_freq(60)

# Initialization
Motor.setup()
Steering.setup(pwm=pwm)
Camera.setup(pwm=pwm)
Led.setup()
Led.police(1)
Ultra.setup()
voice_engine = pyttsx3.init()

class Controller:
    Timers = []

    @staticmethod
    def _cancel_event():
        for timer in Controller.Timers:
            timer.cancel()
        Motor.Timers = []

    @staticmethod
    def _schedule_event(delay, function, args=[], kwargs={}):
        timer = Timer(delay, function, args, kwargs)
        timer.start()
        Controller.Timers.append(timer)

    @staticmethod
    def stop():
        Motor.stop()
        Controller._cancel_event()

    @staticmethod
    def move(direction, speed, heading, duration):
        Camera.set_position(0, -5)
        Motor.move(direction, speed)
        Steering.head(heading)
        Controller._schedule_event(duration, Motor.stop)
        Controller._schedule_event(duration, Steering.middle)

    @staticmethod
    def moves(moves):
        delay = 0
        for move in moves:
            Controller._schedule_event(delay,
                                       Motor.move,
                                       [move['direction'], move['speed']])
            Controller._schedule_event(delay,
                                       Steering.head,
                                       [move['heading']])
            delay += move['duration']
        Controller._schedule_event(delay, Motor.stop)
        Controller._schedule_event(delay, Steering.middle)

    @staticmethod
    def set_camera_position(x, y):
        Camera.set_position(x, y)

    @staticmethod
    def set_led_state(left_on, left_color, right_on, right_color):
        Led.set(left_on, left_color, right_on, right_color)

    @staticmethod
    def say(text):
        config = Config.get_config()
        voice_engine.setProperty('voice', config.get("voice_id", "english_wmids"))
        voice_engine.setProperty('rate', int(config.get("voice_rate", 150)))
        if voice_engine._inLoop:
            voice_engine.endLoop()
        voice_engine.say(text)
        voice_engine.runAndWait()

    @staticmethod
    def get_voices():
        voices = voice_engine.getProperty('voices')
        return [{'age': v.age, 'name': v.name, 'id': v.id, 'languages': v.languages} for v in voices]

    @staticmethod
    def get_distance_map():
        Controller.stop()
        distance_map ={}
        Camera.set_position(-90, -5)
        time.sleep(0.5)
        for a in range(-90, 91, 10):
            Camera.set_position(a, -5)
            time.sleep(0.2)
            distance_map[a] = Ultra.get_distance()
        Camera.set_position(0, 0)

        return distance_map

    @staticmethod
    def serialize():
        return {
            'camera': Camera.serialize(),
            'led': Led.serialize()
        }
