#!/usr/bin/python3
# File name   : setup.py
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : William
# Date        : 2018/10/12

import os
import time

def replace_num(file,initial,new_num):  
    newline=""
    str_num=str(new_num)
    with open(file,"r") as f:
        for line in f.readlines():
            if(line.find(initial) == 0):
                line = (str_num+'\n')
            newline += line
    with open(file,"w") as f:
        f.writelines(newline)
'''
for x in range(1,4):
	if os.system("sudo apt-get update") == 0:
		break

for x in range(1,4):
	if os.system("sudo apt-get -y upgrade") == 0:
		break
'''
for x in range(1,4):
	if os.system("sudo apt-get install -y i2c-tools") == 0:
		break

for x in range(1,4):
	if os.system("sudo pip3 install pip setuptools wheel") == 0:
		break
		
for x in range(1,4):
	if os.system("sudo pip3 install adafruit-pca9685") == 0:
		break

try:
	#replace_num("/boot/config.txt",'#dtparam=spi=on','dtparam=spi=on')
	replace_num("/boot/config.txt",'#dtparam=i2c_arm=on','dtparam=i2c_arm=on\nstart_x=1\n')
	#replace_num("/boot/config.txt",'#dtparam=i2s=on','dtparam=i2s=on')
except:
	print('try again')

for x in range(1,4):
	if os.system("sudo apt-get install -y swig") == 0:
		break

for x in range(1,4):
	if os.system("sudo apt-get install -y bison libasound2-dev swig") == 0:
		break

for x in range(1,4):
	if os.system("sudo apt-get install -y pulseaudio libpulse-dev") == 0:
		break

for x in range(1,4):
	if os.system("sudo apt-get install -y portaudio19-dev python3-all-dev python3-pyaudio") == 0:
		break

for x in range(1,4):
	if os.system("sudo apt-get install -qq python3 python3-dev python3-pip build-essential swig libpulse-dev") == 0:
		break

for x in range(1,4):
	if os.system("sudo apt-get install -y gcc libffi-dev libssl-dev python3-dev") == 0:
		break

for x in range(1,4):
	if os.system("sudo apt-get install pulseaudio pulseaudio-utils libpulse-dev libpulse-java libpulse0") == 0:
		break
		

for x in range(1,4):
	if os.system("sudo apt-get install -y portaudio19-dev python3-all-dev python3-pyaudio") == 0:
		break

for x in range(1,4):
	if os.system("sudo pip3 install pyaudio") == 0:
		break

for x in range(1,4):
	if os.system("sudo apt-get install -y flac") == 0:
		break

for x in range(1,4):
	if os.system("sudo wget https://sourceforge.net/projects/cmusphinx/files/sphinxbase/5prealpha/sphinxbase-5prealpha.tar.gz/download -O sphinxbase.tar.gz") == 0:
		break

for x in range(1,4):
	if os.system("sudo wget https://sourceforge.net/projects/cmusphinx/files/pocketsphinx/5prealpha/pocketsphinx-5prealpha.tar.gz/download -O pocketsphinx.tar.gz") == 0:
		break

for x in range(1,4):
	if os.system("sudo tar -xzvf sphinxbase.tar.gz") == 0:
		break

for x in range(1,4):
	if os.system("sudo tar -xzvf pocketsphinx.tar.gz") == 0:
		break

try:
	os.system("cd sphinxbase-5prealpha/ && ./configure -enable-fixed && make && sudo make install")
	os.system("sudo pip3 install pocketsphinx")
except:
	pass

try:
	os.system("cd pocketsphinx-5prealpha/ && ./configure && make && sudo make install")
	os.system("sudo pip3 install SpeechRecognition")
except:
	pass

try:
	os.system("sudo pip3 install pocketsphinx")
except:
	pass

try:
	os.system("sudo pip3 install SpeechRecognition")
except:
	pass

for x in range(1,4):
	if os.system("sudo apt-get install -y bison libasound2-dev swig") == 0:
		break

for x in range(1,4):
	if os.system("sudo apt-get install -y python3 python3-dev python3-pip build-essential libpulse-dev") == 0:
		break

for x in range(1,4):
	if os.system("sudo apt-get install -y libopencv-dev") == 0:
		break

for x in range(1,4):
	if os.system("sudo apt-get install -y python3-opencv") == 0:
		break

for x in range(1,4):
	if os.system("sudo pip3 install imutils") == 0:
		break
'''
for x in range(1,4):
	if os.system("sudo pip3 install opencv-python") == 0:
		break

for x in range(1,4):
	if os.system("sudo apt-get install -y libatlas-base-dev libjasper-dev libqtgui4 python3-pyqt5 libqt4-test") == 0:
		break
'''
for x in range(1,4):
	if os.system("sudo pip3 install zmq pybase64") == 0:   ####
		break

for x in range(1,4):
	if os.system("sudo pip3 install rpi_ws281x") == 0:
		break

for x in range(1,4):
	if os.system("git clone https://github.com/oblique/create_ap") == 0:
		break

try:
	os.system("cd //home/pi/adeept_picar-b/server/create_ap && sudo make install")
except:
	pass

try:
	os.system("cd //home/pi/create_ap && sudo make install")
except:
	pass

for x in range(1,4):
	if os.system("sudo apt-get install -y util-linux procps hostapd iproute2 iw haveged dnsmasq") == 0:
		break
'''
try:
	os.system('sudo mknod("//home/pi/.config/autostart/car.desktop")')
	with open("//home/pi/.config/autostart/car.desktop",'w') as file_to_write:
		file_to_write.write("[Desktop Entry]\n   Name=Car\n   Comment=Car\n   Exec=sudo python3 //home/pi/adeept_picar-b/server/server.py\n   Icon=false\n   Terminal=false\n   MutipleArgs=false\n   Type=Application\n   Catagories=Application;Development;\n   StartupNotify=true")
except:
	pass
'''
os.system("sudo cp -f //home/pi/adeept_picar-b/server/set.txt /home/pi/set.txt")

try:
	os.system("sudo pip3 install pocketsphinx")
except:
	pass

try:
	os.system('sudo touch //home/pi/startup.sh')
	with open("//home/pi/startup.sh",'w') as file_to_write:
		file_to_write.write("#!/bin/sh\n#sleep 10s\nsudo python3 //home/pi/adeept_picar-b/server/server.py")
except:
	pass

os.system('sudo chmod 777 //home/pi/startup.sh')

replace_num('/etc/rc.local','fi','fi\n//home/pi/startup.sh start')
os.system("sudo cp -f //home/pi/adeept_picar-b/server/set.txt //etc/set.txt")
os.system("sudo cp -f //home/pi/adeept_picar-b/server/set.txt //set.txt")
print('restarting')

os.system("sudo reboot")
