#!/usr/bin/python3
# Product     : PiCar-B
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
import turn
import led
import findline
import os

pwm = Adafruit_PCA9685.PCA9685()    #Ultrasonic Control
#
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
    with open("set.txt","r") as f:
        for line in f.readlines():
            if(line.find(initial) == 0):
                line = initial+"%s" %(str_num+"\n")
            newline += line
    with open("set.txt","w") as f:
        f.writelines(newline)

def num_import_int(initial):        #Call this function to import data from '.txt' file
    with open("set.txt") as f:
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

def findline_thread():       #Line tracking mode
    while 1:
        while findline_mode:
            findline.run()
        time.sleep(0.2)

def auto_thread():           #Ultrasonic tracking mode
    while 1:
        while auto_mode:
            ultra.loop(distance_stay,distance_range)
        time.sleep(0.2)

wifi_status = 0

def run():                   #Main loop
    global hoz_mid,vtr_mid,ip_con,led_status,auto_status,opencv_mode,findline_mode,speech_mode,auto_mode,data,addr,footage_socket,ap_status,turn_status,wifi_status
    led.setup()
    while True:              #Connection      
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

    #Threads start
    findline_threading=threading.Thread(target=findline_thread) #Define a thread for line tracking
    findline_threading.setDaemon(True)                          #'True' means it is a front thread,it would close when the mainloop() closes
    findline_threading.start()                                  #Thread starts

    auto_threading=threading.Thread(target=auto_thread)         #Define a thread for ultrasonic tracking
    auto_threading.setDaemon(True)                              #'True' means it is a front thread,it would close when the mainloop() closes
    auto_threading.start()                                      #Thread starts
    
    time.sleep(0.5)

    tcpCliSock.send('TestVersion'.encode())

    while True: 
        data = ''
        data = tcpCliSock.recv(BUFSIZ).decode()
        if not data:
            continue
        elif 'exit' in data:
            pass

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
            tcpCliSock.send('3'.encode())
        
        elif 'Right' in data:                  #Turn right
            if led_status == 0:
                led.side_color_on(right_R,right_G)
            else:
                led.side_off(right_B)
            turn.right()
            tcpCliSock.send('4'.encode())
        
        elif 'backward' in data:               #When server receive "backward" from client,car moves backward
            tcpCliSock.send('2'.encode())
            motor.motor_left(status, backward, left_spd*spd_ad)
            motor.motor_right(status, forward, right_spd*spd_ad)

        elif 'forward' in data:                #When server receive "forward" from client,car moves forward
            tcpCliSock.send('1'.encode())
            motor.motor_left(status, forward,left_spd*spd_ad)
            motor.motor_right(status,backward,right_spd*spd_ad)

        elif 'l_up' in data:                   #Camera look up
            if vtr_mid< look_up_max:
                vtr_mid+=turn_speed
            turn.camera_turn(vtr_mid)
            tcpCliSock.send('5'.encode())

        elif 'l_do' in data:                   #Camera look down
            if vtr_mid> look_down_max:
                vtr_mid-=turn_speed
            turn.camera_turn(vtr_mid)
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
            findline_mode = 0
            auto_mode     = 0
            auto_status   = 0
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

        elif 'findline' in data:               #Find line mode start
            if auto_status == 0:
                tcpCliSock.send('findline'.encode())
                auto_status = 1
                findline_mode = 1
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

    # LED strip configuration:
    LED_COUNT      = 12      # Number of LED pixels.
    LED_PIN        = 12      # GPIO pin connected to the pixels (18 uses PWM!).
    #LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
    LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
    LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
    LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

    setup()
    try:
        run()
    except KeyboardInterrupt:
        destroy()
