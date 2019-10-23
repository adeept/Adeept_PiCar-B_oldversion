#!/usr/bin/python3
# File name   : server.py
# Description : The main program server takes control of Ultrasonic,Motor,Servo by receiving the order from the client through TCP and carrying out the corresponding operation.
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : William & Tony DiCola (tony@tonydicola.com, the WS_2812 code)
# Date        : 2018/10/12

import RPi.GPIO as GPIO
import motor
import ultra
import socket
import time
import threading
import Adafruit_PCA9685
import picamera
from picamera.array import PiRGBArray
import turn
import led
import findline
import speech
import cv2
from collections import deque
import numpy as np
import argparse
import imutils
from rpi_ws281x import *
import argparse
import zmq
import base64
import os
import subprocess

#time.sleep(4)

pwm = Adafruit_PCA9685.PCA9685()    #Ultrasonic Control

dis_dir = []
distance_stay  = 0.4
distance_range = 2
led_status = 0

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

spd_ad_1 = 1
spd_ad_2 = 1
spd_ad_u = 1

#Status of the car
auto_status   = 0
ap_status     = 0
turn_status   = 0

opencv_mode   = 0
findline_mode = 0
speech_mode   = 0
auto_mode     = 0

data = ''

dis_data = 0
dis_scan = 1

def replace_num(initial,new_num):   #Call this function to replace data in '.txt' file
    newline=""
    str_num=str(new_num)
    with open("//etc/set.txt","r") as f:
        for line in f.readlines():
            if(line.find(initial) == 0):
                line = initial+"%s" %(str_num+"\n")
            newline += line
    with open("set.txt","w") as f:
        f.writelines(newline)

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
ip_con     = ''

def get_ram():
    try:
        s = subprocess.check_output(['free','-m'])
        lines = s.split('\n') 
        return ( int(lines[1].split()[1]), int(lines[2].split()[3]) )
    except:
        return 0

def get_temperature():
    try:
        s = subprocess.check_output(['/opt/vc/bin/vcgencmd','measure_temp'])
        return float(s.split('=')[1][:-3])
    except:
        return 0

def get_cpu_speed():
    f = os.popen('/opt/vc/bin/vcgencmd get_config arm_freq')
    cpu = f.read()
    return cpu



def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        if 'forward' in data:
            for i in range(strip.numPixels()):
                if 'forward' in data:
                    strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
            strip.show()
            time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def colorWipe(strip, color):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(0.005)

def scan():                  #Ultrasonic Scanning
    global dis_dir
    dis_dir = []
    turn.ultra_turn(hoz_mid)   #Ultrasonic point forward
    turn.ultra_turn(look_left_max)   #Ultrasonic point Left,prepare to scan
    dis_dir=['list']         #Make a mark so that the client would know it is a list
    time.sleep(0.5)          #Wait for the Ultrasonic to be in position
    cat_2=look_left_max                #Value of left-position
    GPIO.setwarnings(False)  #Or it may print warnings
    while cat_2>look_right_max:         #Scan,from left to right
        turn.ultra_turn(cat_2)
        cat_2 -= 3           #This value determine the speed of scanning,the greater the faster
        new_scan_data=round(ultra.checkdist(),2)   #Get a distance of a certern direction
        dis_dir.append(str(new_scan_data))              #Put that distance value into a list,and save it as String-Type for future transmission 
    turn.ultra_turn(hoz_mid)   #Ultrasonic point forward
    return dis_dir

def scan_rev():                  #Ultrasonic Scanning
    global dis_dir
    dis_dir = []
    turn.ultra_turn(hoz_mid)   #Ultrasonic point forward
    turn.ultra_turn(look_right_max)   #Ultrasonic point Left,prepare to scan
    dis_dir=['list']         #Make a mark so that the client would know it is a list
    time.sleep(0.5)          #Wait for the Ultrasonic to be in position
    cat_2=look_right_max                #Value of left-position
    GPIO.setwarnings(False)  #Or it may print warnings
    while cat_2<look_left_max:         #Scan,from left to right
        turn.ultra_turn(cat_2)
        cat_2 += 3           #This value determine the speed of scanning,the greater the faster
        new_scan_data=round(ultra.checkdist(),2)   #Get a distance of a certern direction
        dis_dir.append(str(new_scan_data))              #Put that distance value into a list,and save it as String-Type for future transmission 
    turn.ultra_turn(hoz_mid)   #Ultrasonic point forward
    return dis_dir

def ultra_turn(hoz_mid):     #Control the direction of ultrasonic
    pwm.set_pwm(1, 0, hoz_mid)

def camera_turn(vtr_mid):    #Control the direction of Camera
    pwm.set_pwm(0, 0, vtr_mid)

def turn_left_led():         #Turn on the LED on the left
    led.turn_left(4)

def turn_right_led():        #Turn on the LED on the right
    led.turn_right(4)

def setup():                 #initialization
    motor.setup()            
    turn.ahead()
    findline.setup()

def destroy():               #Clean up
    GPIO.cleanup()
    connection.close()
    client_socket.close()

def opencv_thread():         #OpenCV and FPV video
    global hoz_mid_orig,vtr_mid_orig
    font = cv2.FONT_HERSHEY_SIMPLEX
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        cv2.line(image,(300,240),(340,240),(128,255,128),1)
        cv2.line(image,(320,220),(320,260),(128,255,128),1)


        if opencv_mode == 1:
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, colorLower, colorUpper)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)[-2]
            center = None
            if len(cnts) > 0:
                led.both_off()
                led.green()
                cv2.putText(image,'Target Detected',(40,60), font, 0.5,(255,255,255),1,cv2.LINE_AA)
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                X = int(x)
                Y = int(y)
                if radius > 10:
                    cv2.rectangle(image,(int(x-radius),int(y+radius)),(int(x+radius),int(y-radius)),(255,255,255),1)
                    if X < 310:
                        mu1 = int((320-X)/3)
                        hoz_mid_orig+=mu1
                        if hoz_mid_orig < look_left_max:
                            pass
                        else:
                            hoz_mid_orig = look_left_max
                        ultra_turn(hoz_mid_orig)
                        #print('x=%d'%X)
                    elif X >330:
                        mu1 = int((X-330)/3)
                        hoz_mid_orig-=mu1
                        if hoz_mid_orig > look_right_max:
                            pass
                        else:
                            hoz_mid_orig = look_right_max
                        ultra_turn(hoz_mid_orig)
                        #print('x=%d'%X)
                    else:
                        turn.middle()
                        pass

                    mu_t = 390-(hoz_mid-hoz_mid_orig)
                    v_mu_t = 390+(hoz_mid+hoz_mid_orig)
                    turn.turn_ang(mu_t)

                    dis = dis_data
                    if dis < (distance_stay-0.1) :
                        led.both_off()
                        led.red()
                        turn.turn_ang(mu_t)
                        motor.motor_left(status, backward,left_spd*spd_ad_u)
                        motor.motor_right(status,forward,right_spd*spd_ad_u)
                        cv2.putText(image,'Too Close',(40,80), font, 0.5,(128,128,255),1,cv2.LINE_AA)
                    elif dis > (distance_stay+0.1):
                        motor.motor_left(status, forward,left_spd*spd_ad_2)
                        motor.motor_right(status,backward,right_spd*spd_ad_2)
                        cv2.putText(image,'OpenCV Tracking',(40,80), font, 0.5,(128,255,128),1,cv2.LINE_AA)
                    else:
                        motor.motorStop()
                        led.both_off()
                        led.blue()  
                        cv2.putText(image,'In Position',(40,80), font, 0.5,(255,128,128),1,cv2.LINE_AA)

                    if dis < 8:
                        cv2.putText(image,'%s m'%str(round(dis,2)),(40,40), font, 0.5,(255,255,255),1,cv2.LINE_AA)

                    if Y < 230:
                        mu2 = int((240-Y)/5)
                        vtr_mid_orig += mu2
                        if vtr_mid_orig < look_up_max:
                            pass
                        else:
                            vtr_mid_orig=look_up_max
                        camera_turn(vtr_mid_orig)
                    elif Y > 250:
                        mu2 = int((Y-240)/5)
                        vtr_mid_orig -= mu2
                        if vtr_mid_orig > look_down_max:
                            pass
                        else:
                            vtr_mid_orig=look_down_max
                        camera_turn(vtr_mid_orig)
                    
                    if X>280:
                        if X<350:
                            #print('looked')
                            cv2.line(image,(300,240),(340,240),(64,64,255),1)
                            cv2.line(image,(320,220),(320,260),(64,64,255),1)
                            cv2.rectangle(image,(int(x-radius),int(y+radius)),
                                (int(x+radius),int(y-radius)),(64,64,255),1)
            else:
                led.both_off()
                led.yellow()
                cv2.putText(image,'Target Detecting',(40,60), font, 0.5,(255,255,255),1,cv2.LINE_AA)
                led_y=1
                motor.motorStop()

            for i in range(1, len(pts)):
                if pts[i - 1] is None or pts[i] is None:
                    continue
                thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
                cv2.line(image, pts[i - 1], pts[i], (0, 0, 255), thickness)
        else:
            dis = dis_data
            if dis < 8:
                cv2.putText(image,'%s m'%str(round(dis,2)),(40,40), font, 0.5,(255,255,255),1,cv2.LINE_AA)


        encoded, buffer = cv2.imencode('.jpg', image)
        jpg_as_text = base64.b64encode(buffer)
        footage_socket.send(jpg_as_text)
        rawCapture.truncate(0)

def ws2812_thread():         #WS_2812 leds
    while 1:
        if 'forward' in data:
            rainbowCycle(strip)
            time.sleep(0.1)
        elif 'backward' in data:
            colorWipe(strip, Color(255,0,0))
            time.sleep(0.1)
        if turn_status == 1:
            strip.setPixelColor(0, Color(255,255,0))
            strip.setPixelColor(1, Color(255,255,0))
            strip.setPixelColor(2, Color(255,255,0))
        elif turn_status == 2:
            strip.setPixelColor(3, Color(255,255,0))
            strip.setPixelColor(4, Color(255,255,0))
            strip.setPixelColor(5, Color(255,255,0))
        else:
            pass
        time.sleep(0.1)

def findline_thread():       #Line tracking mode
    while 1:
        while findline_mode:
            findline.run()
        time.sleep(0.2)

def speech_thread():         #Speech recognition mode
    while 1:
        while speech_mode:
            speech.run()
        time.sleep(0.2)

def auto_thread():           #Ultrasonic tracking mode
    while 1:
        while auto_mode:
            ultra.loop(distance_stay,distance_range)
        time.sleep(0.2)

def dis_scan_thread():       #Get Ultrasonic scan distance
    global dis_data
    while 1:
        while  dis_scan:
            dis_data = ultra.checkdist()
            time.sleep(0.2)
        time.sleep(0.2)

def ap_thread():             #Set up an AP-Hotspot
    os.system("sudo create_ap wlan0 eth0 AdeeptCar 12345678")

wifi_status = 0

def run():                   #Main loop
    global hoz_mid,vtr_mid,ip_con,led_status,auto_status,opencv_mode,findline_mode,speech_mode,auto_mode,data,addr,footage_socket,ap_status,turn_status,wifi_status
    led.setup()
    while True:              #Connection
        try:
            s =socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            s.connect(("1.1.1.1",80))
            ipaddr_check=s.getsockname()[0]
            s.close()
            print(ipaddr_check)
            wifi_status=1
        except:
            if ap_status == 0:
                ap_threading=threading.Thread(target=ap_thread)   #Define a thread for data receiving
                ap_threading.setDaemon(True)                          #'True' means it is a front thread,it would close when the mainloop() closes
                ap_threading.start()                                  #Thread starts
                led.both_off()
                led.yellow()
                time.sleep(5)
                wifi_status = 0
            
        if wifi_status == 1:
            print('waiting for connection...')
            led.red()
            tcpCliSock, addr = tcpSerSock.accept()#Determine whether to connect
            led.both_off()
            led.green()
            print('...connected from :', addr)
            #time.sleep(1)
            tcpCliSock.send(('SET %s'%vtr_mid+' %s'%hoz_mid+' %s'%left_spd+' %s'%right_spd+' %s'%look_up_max+' %s'%look_down_max).encode())
            print('SET %s'%vtr_mid+' %s'%hoz_mid+' %s'%left_spd+' %s'%right_spd+' %s'%left+' %s'%right)
            break
        else:
            led.both_off()
            led.blue()
            print('waiting for connection...')
            tcpCliSock, addr = tcpSerSock.accept()#Determine whether to connect
            led.both_off()
            led.green()
            print('...connected from :', addr)
            #time.sleep(1)
            tcpCliSock.send(('SET %s'%vtr_mid+' %s'%hoz_mid+' %s'%left_spd+' %s'%right_spd+' %s'%look_up_max+' %s'%look_down_max).encode())
            print('SET %s'%vtr_mid+' %s'%hoz_mid+' %s'%left_spd+' %s'%right_spd+' %s'%left+' %s'%right)
            ap_status = 1
            break


    #FPV initialization
    context = zmq.Context()
    footage_socket = context.socket(zmq.PUB)
    footage_socket.connect('tcp://%s:5555'%addr[0])
    print(addr[0])
    #Threads start
    video_threading=threading.Thread(target=opencv_thread)      #Define a thread for FPV and OpenCV
    video_threading.setDaemon(True)                             #'True' means it is a front thread,it would close when the mainloop() closes
    video_threading.start()                                     #Thread starts

    ws2812_threading=threading.Thread(target=ws2812_thread)     #Define a thread for ws_2812 leds
    ws2812_threading.setDaemon(True)                            #'True' means it is a front thread,it would close when the mainloop() closes
    ws2812_threading.start()                                    #Thread starts

    findline_threading=threading.Thread(target=findline_thread) #Define a thread for line tracking
    findline_threading.setDaemon(True)                          #'True' means it is a front thread,it would close when the mainloop() closes
    findline_threading.start()                                  #Thread starts

    speech_threading=threading.Thread(target=speech_thread)     #Define a thread for speech recognition
    speech_threading.setDaemon(True)                            #'True' means it is a front thread,it would close when the mainloop() closes
    speech_threading.start()                                    #Thread starts

    auto_threading=threading.Thread(target=auto_thread)         #Define a thread for ultrasonic tracking
    auto_threading.setDaemon(True)                              #'True' means it is a front thread,it would close when the mainloop() closes
    auto_threading.start()                                      #Thread starts

    scan_threading=threading.Thread(target=dis_scan_thread)     #Define a thread for ultrasonic scan
    scan_threading.setDaemon(True)                              #'True' means it is a front thread,it would close when the mainloop() closes
    scan_threading.start()                                      #Thread starts


    while True: 
        data = ''
        data = tcpCliSock.recv(BUFSIZ).decode()
        if not data:
            continue
        elif 'exit' in data:
            os.system("sudo shutdown -h now\n")

        elif 'spdset' in data:
            global spd_ad
            spd_ad=float((str(data))[7:])      #Speed Adjustment

        elif 'scan' in data:
            dis_can=scan()                     #Start Scanning
            str_list_1=dis_can                 #Divide the list to make it samller to send 
            str_index=' '                      #Separate the values by space
            str_send_1=str_index.join(str_list_1)+' '
            tcpCliSock.sendall((str(str_send_1)).encode())   #Send Data
            tcpCliSock.send('finished'.encode())        #Sending 'finished' tell the client to stop receiving the list of dis_can

        elif 'scan_rev' in data:
            dis_can=scan_rev()                     #Start Scanning
            str_list_1=dis_can                 #Divide the list to make it samller to send 
            str_index=' '                      #Separate the values by space
            str_send_1=str_index.join(str_list_1)+' '
            tcpCliSock.sendall((str(str_send_1)).encode())   #Send Data
            tcpCliSock.send('finished'.encode())        #Sending 'finished' tell the client to stop receiving the list of dis_can

        elif 'EC1set' in data:                 #Camera Adjustment
            new_EC1=int((str(data))[7:])
            turn.camera_turn(new_EC1)
            replace_num('E_C1:',new_EC1)

        elif 'EC2set' in data:                 #Ultrasonic Adjustment
            new_EC2=int((str(data))[7:])
            replace_num('E_C2:',new_EC2)
            turn.ultra_turn(new_EC2)

        elif 'EM1set' in data:                 #Motor A Speed Adjustment
            new_EM1=int((str(data))[7:])
            replace_num('E_M1:',new_EM1)

        elif 'EM2set' in data:                 #Motor B Speed Adjustment
            new_EM2=int((str(data))[7:])
            replace_num('E_M2:',new_EM2)

        elif 'LUMset' in data:                 #Motor A Turningf Speed Adjustment
            new_ET1=int((str(data))[7:])
            replace_num('look_up_max:',new_ET1)
            turn.camera_turn(new_ET1)

        elif 'LDMset' in data:                 #Motor B Turningf Speed Adjustment
            new_ET2=int((str(data))[7:])
            replace_num('look_down_max:',new_ET2)
            turn.camera_turn(new_ET2)

        elif 'stop' in data:                   #When server receive "stop" from client,car stops moving
            tcpCliSock.send('9'.encode())
            setup()
            motor.motorStop()
            setup()
            if led_status == 0:
                led.setup()
                led.both_off()
            colorWipe(strip, Color(0,0,0))
            continue
        
        elif 'lightsON' in data:               #Turn on the LEDs
            led.both_on()
            led_status=1
            tcpCliSock.send('lightsON'.encode())

        elif 'lightsOFF'in data:               #Turn off the LEDs
            led.both_off()
            led_status=0
            tcpCliSock.send('lightsOFF'.encode())

        elif 'middle' in data:                 #Go straight
            if led_status == 0:
                led.side_color_off(left_R,left_G)
                led.side_color_off(right_R,right_G)
            else:
                led.side_on(left_B)
                led.side_on(right_B)
            turn_status = 0
            turn.middle()
        
        elif 'Left' in data:                   #Turn left
            if led_status == 0:
                led.side_color_on(left_R,left_G)
            else:
                led.side_off(left_B)
            turn.left()
            turn_status=1
            tcpCliSock.send('3'.encode())
        
        elif 'Right' in data:                  #Turn right
            if led_status == 0:
                led.side_color_on(right_R,right_G)
            else:
                led.side_off(right_B)
            turn.right()
            turn_status=2
            tcpCliSock.send('4'.encode())
        
        elif 'backward' in data:               #When server receive "backward" from client,car moves backward
            tcpCliSock.send('2'.encode())
            motor.motor_left(status, backward, left_spd*spd_ad)
            motor.motor_right(status, forward, right_spd*spd_ad)
            colorWipe(strip, Color(255,0,0))

        elif 'forward' in data:                #When server receive "forward" from client,car moves forward
            tcpCliSock.send('1'.encode())
            motor.motor_left(status, forward,left_spd*spd_ad)
            motor.motor_right(status,backward,right_spd*spd_ad)
            colorWipe(strip, Color(0,0,255))

        elif 'l_up' in data:                   #Camera look up
            if vtr_mid< look_up_max:
                vtr_mid+=turn_speed
            turn.camera_turn(vtr_mid)
            tcpCliSock.send('5'.encode())

        elif 'l_do' in data:                   #Camera look down
            if vtr_mid> look_down_max:
                vtr_mid-=turn_speed
            turn.camera_turn(vtr_mid)
            print(vtr_mid)
            tcpCliSock.send('6'.encode())

        elif 'l_le' in data:                   #Camera look left
            if hoz_mid< look_left_max:
                hoz_mid+=turn_speed
            turn.ultra_turn(hoz_mid)
            tcpCliSock.send('7'.encode())

        elif 'l_ri' in data:                   #Camera look right
            if hoz_mid> look_right_max:
                hoz_mid-=turn_speed
            turn.ultra_turn(hoz_mid)
            tcpCliSock.send('8'.encode())

        elif 'ahead' in data:                  #Camera look ahead
            turn.ahead()

        elif 'Stop' in data:                   #When server receive "Stop" from client,Auto Mode switches off
            opencv_mode   = 0
            findline_mode = 0
            speech_mode   = 0
            auto_mode     = 0
            auto_status   = 0
            dis_scan = 1
            tcpCliSock.send('auto_status_off'.encode())
            motor.motorStop()
            led.both_off()
            turn.middle()
            time.sleep(0.1)
            motor.motorStop()
            led.both_off()
            turn.middle()
        
        elif 'auto' in data:                   #When server receive "auto" from client,start Auto Mode
            if auto_status == 0:
                tcpCliSock.send('0'.encode())
                auto_status = 1
                auto_mode = 1
                dis_scan = 0
            else:
                pass
            continue

        elif 'opencv' in data:                 #When server receive "auto" from client,start Auto Mode
            if auto_status == 0:
                auto_status = 1
                opencv_mode = 1                  
                tcpCliSock.send('oncvon'.encode())
            continue

        elif 'findline' in data:               #Find line mode start
            if auto_status == 0:
                tcpCliSock.send('findline'.encode())
                auto_status = 1
                findline_mode = 1
            else:
                pass
            continue

        elif 'voice_3' in data:                #Speech recognition mode start
            if auto_status == 0:
                auto_status = 1
                speech_mode = 1
                tcpCliSock.send('voice_3'.encode())
            else:
                pass
            continue

if __name__ == '__main__':

    HOST = ''
    PORT = 10223                              #Define port serial 
    BUFSIZ = 1024                             #Define buffer size
    ADDR = (HOST, PORT)

    tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpSerSock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    tcpSerSock.bind(ADDR)
    tcpSerSock.listen(5)                      #Start server,waiting for client

    camera = picamera.PiCamera()              #Camera initialization
    camera.resolution = (640, 480)
    camera.framerate = 7
    rawCapture = PiRGBArray(camera, size=(640, 480))

    colorLower = (24, 100, 100)               #The color that openCV find
    colorUpper = (44, 255, 255)               #USE HSV value NOT RGB

    ap = argparse.ArgumentParser()            #OpenCV initialization
    ap.add_argument("-b", "--buffer", type=int, default=64,
        help="max buffer size")
    args = vars(ap.parse_args())
    pts = deque(maxlen=args["buffer"])
    time.sleep(0.1)

    # LED strip configuration:
    LED_COUNT      = 12      # Number of LED pixels.
    LED_PIN        = 12      # GPIO pin connected to the pixels (18 uses PWM!).
    #LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
    LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
    LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
    LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    setup()
    try:
        run()
    except KeyboardInterrupt:
        if ap_status == 1:
            os.system("sudo shutdown -h now\n")
            time.sleep(5)
            print('shutdown')
        colorWipe(strip, Color(0,0,0))
        camera=picamera.PiCamera()
        camera.close()
        destroy()
