#!/usr/bin/env/python
# File name   : appserver.py
# Production  : PiCar-B
# Website     : www.adeept.com
# Author      : William
# Date        : 2019/10/28

import socket
import threading
import time
import os
import LEDapp as LED
import led
import motor
import turn


motor.setup()            
turn.ahead()
LED  = LED.LED()
LED.colorWipe(80,255,0)
led.setup()

step_set = 1
speed_set = 100
rad = 0.6

direction_command = 'no'
turn_command = 'no'
servo_command = 'no'
pos_input = 1
catch_input = 1
cir_input = 6

servo_speed  = 11


def num_import_int(initial):        #Call this function to import data from '.txt' file
    with open("//etc/set.txt") as f:
        for line in f.readlines():
            if(line.find(initial) == 0):
                r=line
    begin=len(list(initial))
    snum=r[begin:]
    n=int(snum)
    return n


vtr_mid    = num_import_int('E_C1:')
hoz_mid    = num_import_int('E_C2:')
look_up_max    = num_import_int('look_up_max:')
look_down_max  = num_import_int('look_down_max:')
look_right_max = num_import_int('look_right_max:')
look_left_max  = num_import_int('look_left_max:')
turn_speed     = num_import_int('look_turn_speed:')

vtr_mid_orig = vtr_mid
hoz_mid_orig = hoz_mid

left_R = 22
left_G = 23
left_B = 24

right_R = 10
right_G = 9
right_B = 25

spd_ad     = 1          #Speed Adjustment
pwm0       = 0          #Camera direction 
pwm1       = 1          #Ultrasonic direction
status     = 1          #Motor rotation
forward    = 1          #Motor forward
backward   = 0          #Motor backward

left_spd   = 100         #Speed of the car
right_spd  = 100         #Speed of the car
left       = 100         #Motor Left
right      = 100         #Motor Right


class Servo_ctrl(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(Servo_ctrl, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()     # 用于暂停线程的标识
        self.__flag.set()       # 设置为True
        self.__running = threading.Event()      # 用于停止线程的标识
        self.__running.set()      # 将running设置为True

    def run(self):
        global hoz_mid, vtr_mid
        while self.__running.isSet():
            self.__flag.wait()      # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
            if servo_command == 'lookleft':
                if hoz_mid< look_left_max:
                    hoz_mid+=turn_speed
                turn.ultra_turn(hoz_mid)
            elif servo_command == 'lookright':
                if hoz_mid> look_right_max:
                    hoz_mid-=turn_speed
                turn.ultra_turn(hoz_mid)
            elif servo_command == 'up':
                if vtr_mid< look_up_max:
                    vtr_mid+=turn_speed
                turn.camera_turn(vtr_mid)
            elif servo_command == 'down':
                if vtr_mid> look_down_max:
                    vtr_mid-=turn_speed
                turn.camera_turn(vtr_mid)
            time.sleep(0.07)

    def pause(self):
        self.__flag.clear()     # 设置为False, 让线程阻塞

    def resume(self):
        self.__flag.set()    # 设置为True, 让线程停止阻塞

    def stop(self):
        self.__flag.set()       # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()        # 设置为False  


def app_ctrl():
    global servo_move
    app_HOST = ''
    app_PORT = 10123
    app_BUFSIZ = 1024
    app_ADDR = (app_HOST, app_PORT)

    servo_move = Servo_ctrl()
    servo_move.start()
    servo_move.pause()

    def  ap_thread():
        os.system("sudo create_ap wlan0 eth0 Adeept 12345678")

    def setup():
        motor.setup()

    def appCommand(data_input):
        global direction_command, turn_command, servo_command
        if data_input == 'forwardStart\n':
            motor.motor_left(status, forward,left_spd*spd_ad)
            motor.motor_right(status,backward,right_spd*spd_ad)
            LED.colorWipe(0,80,255)

        elif data_input == 'backwardStart\n':
            motor.motor_left(status, backward, left_spd*spd_ad)
            motor.motor_right(status, forward, right_spd*spd_ad)
            LED.colorWipe(255,80,0)

        elif data_input == 'leftStart\n':
            turn.left()

        elif data_input == 'rightStart\n':
            turn.right()

        elif 'forwardStop' in data_input:
            motor.motorStop()

        elif 'backwardStop' in data_input:
            motor.motorStop()

        elif 'leftStop' in data_input:
            turn.middle()

        elif 'rightStop' in data_input:
            turn.middle()


        if data_input == 'lookLeftStart\n':
            servo_command = 'lookleft'
            servo_move.resume()

        elif data_input == 'lookRightStart\n': 
            servo_command = 'lookright'
            servo_move.resume()

        elif data_input == 'downStart\n':
            servo_command = 'down'
            servo_move.resume()

        elif data_input == 'upStart\n':
            servo_command = 'up'
            servo_move.resume()

        elif 'lookLeftStop' in data_input:
            servo_move.pause()
            servo_command = 'no'
        elif 'lookRightStop' in data_input:
            servo_move.pause()
            servo_command = 'no'
        elif 'downStop' in data_input:
            servo_move.pause()
            servo_command = 'no'
        elif 'upStop' in data_input:
            servo_move.pause()
            servo_command = 'no'


        if data_input == 'aStart\n':
            led.both_on()

        elif data_input == 'bStart\n':
            led.both_off()

        elif data_input == 'cStart\n':
            pass

        elif data_input == 'dStart\n':
            pass

        elif 'aStop' in data_input:
            pass
        elif 'bStop' in data_input:
            pass
        elif 'cStop' in data_input:
            pass
        elif 'dStop' in data_input:
            pass

        print(data_input)

    def appconnect():
        global AppCliSock, AppAddr
        try:
            s =socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            s.connect(("1.1.1.1",80))
            ipaddr_check=s.getsockname()[0]
            s.close()
            print(ipaddr_check)

            AppSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            AppSerSock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            AppSerSock.bind(app_ADDR)
            AppSerSock.listen(5)
            print('waiting for App connection...')
            AppCliSock, AppAddr = AppSerSock.accept()
            print('...App connected from :', AppAddr)
        except:
            ap_threading=threading.Thread(target=ap_thread)   #Define a thread for data receiving
            ap_threading.setDaemon(True)                          #'True' means it is a front thread,it would close when the mainloop() closes
            ap_threading.start()                                  #Thread starts

            LED.colorWipe(0,16,50)
            time.sleep(1)
            LED.colorWipe(0,16,100)
            time.sleep(1)
            LED.colorWipe(0,16,150)
            time.sleep(1)
            LED.colorWipe(0,16,200)
            time.sleep(1)
            LED.colorWipe(0,16,255)
            time.sleep(1)
            LED.colorWipe(35,255,35)

            AppSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            AppSerSock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            AppSerSock.bind(app_ADDR)
            AppSerSock.listen(5)
            print('waiting for App connection...')
            AppCliSock, AppAddr = AppSerSock.accept()
            print('...App connected from :', AppAddr)

    appconnect()
    setup()
    app_threading=threading.Thread(target=appconnect)         #Define a thread for FPV and OpenCV
    app_threading.setDaemon(True)                             #'True' means it is a front thread,it would close when the mainloop() closes
    app_threading.start()                                     #Thread starts

    while 1:
        data = ''
        data = str(AppCliSock.recv(app_BUFSIZ).decode())
        if not data:
            continue
        appCommand(data)
        pass

AppConntect_threading=threading.Thread(target=app_ctrl)         #Define a thread for FPV and OpenCV
AppConntect_threading.setDaemon(True)                             #'True' means it is a front thread,it would close when the mainloop() closes
AppConntect_threading.start()                                     #Thread starts

if __name__ == '__main__':
    i = 1
    try:
        while 1:
            i += 1
            print(i)
            time.sleep(30)
            pass
    except:
        servo_move.stop()
        motor.motorStop()
        LED.colorWipe(0,0,0)