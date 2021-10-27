#!/usr/bin/python3
# File name   : motor.py
# Description : Control LEDs 
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : William
# Date        : 2018/10/12
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
        Led.state = {
            'left_r': 'off',
            'left_g': 'off',
            'left_b': 'off',
            'right_r': 'off',
            'right_g': 'off',
            'right_b': 'off'
        }

    @staticmethod
    def both_on():
        GPIO.output(left_R, on)
        GPIO.output(left_G, on)
        GPIO.output(left_B, on)

        GPIO.output(right_R, on)
        GPIO.output(right_G, on)
        GPIO.output(right_B, on)

    @staticmethod
    def set(left_r, left_g, left_b, right_r, right_g, right_b):
        Led.state = {
            'left_r': left_r,
            'left_g': left_g,
            'left_b': left_b,
            'right_r': right_r,
            'right_g': right_g,
            'right_b': right_b
        }
        Led._output()

    @staticmethod
    def _output():
        GPIO.output(left_R, on if Led.state.get('left_r') == "on" else off)
        GPIO.output(left_G, on if Led.state.get('left_g') == "on" else off)
        GPIO.output(left_B, on if Led.state.get('left_b') == "on" else off)

        GPIO.output(right_R, on if Led.state.get('right_r') == "on" else off)
        GPIO.output(right_G, on if Led.state.get('right_g') == "on" else off)
        GPIO.output(right_B, on if Led.state.get('right_b') == "on" else off)

    @staticmethod
    def serialize():
        return {
            'state': Led.state
        }

    @staticmethod
    def both_off():
        GPIO.output(left_R, off)
        GPIO.output(left_G, off)
        GPIO.output(left_B, off)

        GPIO.output(right_R, off)
        GPIO.output(right_G, off)
        GPIO.output(right_B, off)

    @staticmethod
    def police(police_time):
        for i in range(1, police_time):
            for j in range(1, 3):
                Led.side_on(left_R)
                Led.side_on(right_B)
                time.sleep(0.1)
                Led.both_off()
                Led.side_on(left_B)
                Led.side_on(right_R)
                time.sleep(0.1)
                Led.both_off()
            for j in range(1, 5):
                Led.side_on(left_R)
                Led.side_on(right_B)
                time.sleep(0.3)
                Led.both_off()
                Led.side_on(left_B)
                Led.side_on(right_R)
                time.sleep(0.3)
                Led.both_off()

    @staticmethod
    def red():
        Led.side_on(right_R)
        Led.side_on(left_R)

    @staticmethod
    def green():
        Led.side_on(right_G)
        Led.side_on(left_G)

    @staticmethod
    def blue():
        Led.side_on(right_B)
        Led.side_on(left_B)

    @staticmethod
    def yellow():
        Led.red()
        Led.green()

    @staticmethod
    def pink():
        Led.red()
        Led.blue()

    @staticmethod
    def cyan():
        Led.blue()
        Led.green()

    @staticmethod
    def side_color_on(side_x, side_y):
        GPIO.output(side_x, on)
        GPIO.output(side_y, on)

    @staticmethod
    def side_color_off(side_x, side_y):
        GPIO.output(side_x, off)
        GPIO.output(side_y, off)

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
