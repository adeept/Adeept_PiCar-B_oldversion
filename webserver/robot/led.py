#!/usr/bin/python3
# File name   : motor.py
# Description : Control LEDs 
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : William
# Date        : 2018/10/12
try:
    import RPi.GPIO as GPIO
except:
    import sys
    import fake_rpi
    sys.modules['RPi'] = fake_rpi.RPi
    sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO
    import RPi.GPIO as GPIO
import time

left_R = 22
left_G = 23
left_B = 24

right_R = 10
right_G = 9
right_B = 25

on = GPIO.LOW
off = GPIO.HIGH

COLOR_MAP = {
    'white': [True, True, True],
    'red': [True, False, False],
    'green': [False, True, False],
    'blue': [False, False, True],
    'cyan': [False, True, True],
    'pink': [True, False, True],
    'yellow': [True, True, False]
}

class Led(object):
    state = {}

    @staticmethod
    def setup():  # Initialization
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(left_R, GPIO.OUT)
        GPIO.setup(left_G, GPIO.OUT)
        GPIO.setup(left_B, GPIO.OUT)
        GPIO.setup(right_R, GPIO.OUT)
        GPIO.setup(right_G, GPIO.OUT)
        GPIO.setup(right_B, GPIO.OUT)
        Led.both_off()

    @staticmethod
    def both_on():
        GPIO.output(left_R, on)
        GPIO.output(left_G, on)
        GPIO.output(left_B, on)

        GPIO.output(right_R, on)
        GPIO.output(right_G, on)
        GPIO.output(right_B, on)
        Led.state = {
            'left_on': True,
            'left_color': 'white',
            'right_on': True,
            'right_color': 'white'
        }

    @staticmethod
    def both_off():
        GPIO.output(left_R, off)
        GPIO.output(left_G, off)
        GPIO.output(left_B, off)

        GPIO.output(right_R, off)
        GPIO.output(right_G, off)
        GPIO.output(right_B, off)
        Led.state = {
            'left_on': False,
            'left_color': 'white',
            'right_on': False,
            'right_color': 'white'
        }

    @staticmethod
    def set(left_on, left_color, right_on, right_color):
        Led.state = {
            'left_on': left_on,
            'left_color': left_color,
            'right_on': right_on,
            'right_color': right_color,
        }
        Led._output()

    @staticmethod
    def _output():
        r_on, g_on, b_on = COLOR_MAP[Led.state.get('left_color')] if Led.state.get('left_on') else [False, False, False]
        GPIO.output(left_R, on if r_on else off)
        GPIO.output(left_G, on if g_on else off)
        GPIO.output(left_B, on if b_on else off)

        r_on, g_on, b_on = COLOR_MAP[Led.state.get('right_color')] if Led.state.get('right_on') else [False, False, False]
        GPIO.output(right_R, on if r_on else off)
        GPIO.output(right_G, on if g_on else off)
        GPIO.output(right_B, on if b_on else off)

    @staticmethod
    def serialize():
        return {
            'state': Led.state
        }

    @staticmethod
    def police(police_time):
        for i in range(0, police_time):
            for j in range(1, 3):
                Led.set(left_on=True, left_color='red', right_on=True, right_color="blue")
                time.sleep(0.1)
                Led.both_off()
                Led.set(left_on=True, left_color='blue', right_on=True, right_color="red")
                time.sleep(0.1)
                Led.both_off()
            for j in range(1, 5):
                Led.set(left_on=True, left_color='red', right_on=True, right_color="blue")
                time.sleep(0.3)
                Led.both_off()
                Led.set(left_on=True, left_color='blue', right_on=True, right_color="red")
                time.sleep(0.3)
                Led.both_off()

    @staticmethod
    def turn_left(times):
        for i in range(0, times):
            Led.both_off()
            Led.side_on(left_G)
            Led.side_on(left_R)
            time.sleep(0.5)
            Led.both_off()
            time.sleep(0.5)

    @staticmethod
    def turn_right(times):
        for i in range(1, times):
            Led.both_off()
            Led.side_on(right_G)
            Led.side_on(right_R)
            time.sleep(0.5)
            Led.both_off()
            time.sleep(0.5)
