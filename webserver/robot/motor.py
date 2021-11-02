#!/usr/bin/python3
# File name   : motor.py
# Description : Control Motors 
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : William
# Date        : 2018/10/12
import time

import RPi.GPIO as GPIO


# motor_EN_A: Pin7  |  motor_EN_B: Pin11
# motor_A:  Pin8,Pin10    |  motor_B: Pin13,Pin12


class Motor(object):
	EN = 17
	Pin1 = 27
	Pin2 = 18
	PWM = 0
	direction = 'S'
	speed = 0

	@staticmethod
	def setup():  # Motor initialization
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(Motor.EN, GPIO.OUT)
		GPIO.setup(Motor.Pin1, GPIO.OUT)
		GPIO.setup(Motor.Pin2, GPIO.OUT)
		try:
			Motor.PWM = GPIO.PWM(Motor.EN, 1000)
		except:
			pass
		Motor.stop()

	@staticmethod
	def stop():  # Motor stops
		Motor.direction = 'S'
		Motor.speed = 0
		GPIO.output(Motor.Pin1, GPIO.LOW)
		GPIO.output(Motor.Pin2, GPIO.LOW)
		GPIO.output(Motor.EN, GPIO.LOW)

	@staticmethod
	def emergency_stop():  # Motor stops
		if Motor.direction == 'F':
			Motor.move('B', 100)
		elif Motor.direction == 'B':
			Motor.move('F', 100)
		time.sleep(0.2)
		Motor.stop()

	@staticmethod
	def move(direction, speed):  # Motor positive and negative rotation
		Motor.direction = direction
		Motor.speed = speed
		if direction == 'S':  # stop
			Motor.stop()
		else:
			if direction == 'B':
				GPIO.output(Motor.Pin1, GPIO.HIGH)
				GPIO.output(Motor.Pin2, GPIO.LOW)
				Motor.PWM.start(100)
				Motor.PWM.ChangeDutyCycle(speed)
			elif direction == 'F':
				GPIO.output(Motor.Pin1, GPIO.LOW)
				GPIO.output(Motor.Pin2, GPIO.HIGH)
				Motor.PWM.start(0)
				Motor.PWM.ChangeDutyCycle(speed)
