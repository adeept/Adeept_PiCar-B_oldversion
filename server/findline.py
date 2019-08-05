#!/usr/bin/python3
# File name   : findline.py
# Description : line tracking 
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : William
# Date        : 2018/10/12
import RPi.GPIO as GPIO
import time
import motor
import turn
import led

def num_import_int(initial):        #Call this function to import data from '.txt' file
    with open("set.txt") as f:
        for line in f.readlines():
            if(line.find(initial) == 0):
                r=line
    begin=len(list(initial))
    snum=r[begin:]
    n=int(snum)
    return n

status     = 1          #Motor rotation
forward    = 1          #Motor forward
backward   = 0          #Motor backward

left_spd   = num_import_int('E_M1:')         #Speed of the car
right_spd  = num_import_int('E_M2:')         #Speed of the car
left       = num_import_int('E_T1:')         #Motor Left
right      = num_import_int('E_T2:')         #Motor Right

line_pin_right = 19
line_pin_middle = 16
line_pin_left = 20

left_R = 22
left_G = 23
left_B = 24

right_R = 10
right_G = 9
right_B = 25

on  = GPIO.LOW
off = GPIO.HIGH

spd_ad_1 = 1
spd_ad_2 = 1

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(line_pin_right,GPIO.IN)
    GPIO.setup(line_pin_middle,GPIO.IN)
    GPIO.setup(line_pin_left,GPIO.IN)
    try:
        motor.setup()
    except:
        pass

def run():
    status_right = GPIO.input(line_pin_right)
    status_middle = GPIO.input(line_pin_middle)
    status_left = GPIO.input(line_pin_left)
    if status_left == 1:
        turn.left()
        led.both_off()
        led.side_on(left_R)
        motor.motor_left(status, forward,left_spd*spd_ad_2)
        motor.motor_right(status,backward,right_spd*spd_ad_2)
    elif status_middle == 1:
        turn.middle()
        led.both_off()
        led.yellow()
        motor.motor_left(status, forward,left_spd*spd_ad_1)
        motor.motor_right(status,backward,right_spd*spd_ad_1)
    elif status_right == 1:
        turn.right()
        led.both_off()
        led.side_on(right_R)
        motor.motor_left(status, forward,left_spd*spd_ad_2)
        motor.motor_right(status,backward,right_spd*spd_ad_2)
    else:
        turn.middle()
        led.both_off()
        led.cyan()
        motor.motor_left(status, backward,left_spd)
        motor.motor_right(status,forward,right_spd)
    pass

try:
    pass
except KeyboardInterrupt:
    motor.motorStop()
