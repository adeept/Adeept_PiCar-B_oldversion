#!/usr/bin/python3
# File name   : Ultrasonic.py
# Description : Detection distance and tracking with ultrasonic
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

Tr = 11
Ec = 8


class Ultra(object):
    TIMEOUT = 0.2

    @staticmethod
    def setup():
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Tr, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(Ec, GPIO.IN)

    @staticmethod
    def get_distance():  # Reading distance
        GPIO.output(Tr, GPIO.HIGH)
        time.sleep(0.000015)
        GPIO.output(Tr, GPIO.LOW)
        while not GPIO.input(Ec):
            pass
        t1 = time.time()
        while GPIO.input(Ec) or (time.time() - t1) > Ultra.TIMEOUT:
            pass
        t2 = time.time()
        return (t2 - t1) * 340/2
