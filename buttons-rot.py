#!/usr/bin/python
# button-rasp
# December 28, 2014
# March 1st, 2015 add seek with a long press on next and prev buttons
# Remix by Balbuze (balbuze@gmail.com)2014 December 
# written for Raspberry B+ :for other model please re-assign gpio port!!!
# add physical buttons for a mdp player system (used with Volumio)
# Provide :	-previous / seek -8 sec with long press
#		-next / seek +8 sec with long press
#		-stop
#		-play
#		-volume control through rotary coder 
# My first python script !!! Surely not perfect....To be improve
#
# inspirated from :
#
# Connecting a Push Switch http://razzpisampler.oreilly.com/ch07.html
# Tutorial: Raspberry Pi GPIO PINS AND PYTHON http://makezine.com/projects/tutorial-raspberry-pi-gpio-pins-and-python/
#
# radio.py  
# January 23, 2013  
# Written by Sheldon Hartling for Usual Panic.  
# MIT license, all text above must be included in any redistribution  
# 
#  
# based on code from Kyle Prier (http://wwww.youtube.com/meistervision)  
# and AdaFruit Industries (https://www.adafruit.com)  
# Kyle Prier - https://www.dropbox.com/s/w2y8xx7t6gkq8yz/radio.py  
# AdaFruit   - https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code.git, Adafruit_CharLCD
# Rotary class part from : Author : Bob Rathbone
# Site : http://www.bobrathbone.com
#  

import RPi.GPIO as GPIO
import sys,os
#import mpd
import time
#import random
from rotary_class import RotaryEncoder  
import subprocess
#----------------------------------------------------
# The below setting is to work with iqaudio pi-dac+ and iqaudio pi-amp+
GPIO.setmode(GPIO.BCM)  
# Define GPIO output pins for Radio Controls  
SW_PREV = 12  # Pin 32
SW_NEXT = 16 # Pin 36
SW_STOP = 13 # Pin 33
SW_SHTDWN = 5 # Pin 29
SW_PLAY = 26 # Pin 37
SW_REB = 6 # Pin 31
# Define GPIO for rotary encoder + button
PIN_A = 23  # Pin 16
PIN_B = 24  # Pin 18
BUTTON = 25 # Pin 22
#------------------------------------------------------------

#------------------------------------------------------------
#
#Code to manage Rotary encoder + switch

# This is the event callback routine to handle events
def switch_event(event):
        if event == RotaryEncoder.CLOCKWISE:
		tmp =""
		subprocess.call(['mpc', 'volume', '+2' ])
		time.sleep(.2)
        elif event == RotaryEncoder.ANTICLOCKWISE:
		tmp =""
		subprocess.call(['mpc', 'volume', '-2' ])
		time.sleep(.2)
        return
# Define the switch
rswitch = RotaryEncoder(PIN_A,PIN_B,BUTTON,switch_event)
#----------------------------------------------------------
#
#code to manage BUTTONS previous,next,stop,play,shutdown
GPIO.setup(SW_PREV,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW_NEXT,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW_STOP,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW_SHTDWN,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW_PLAY,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW_REB,GPIO.IN, pull_up_down=GPIO.PUD_UP)
while True:
	try:
		prev_switch = GPIO.input(SW_PREV)
		next_switch = GPIO.input(SW_NEXT)
		stop_switch = GPIO.input(SW_STOP)
		shtdwn_switch = GPIO.input(SW_SHTDWN)
		play_switch = GPIO.input(SW_PLAY)
		reb_switch = GPIO.input(SW_REB)
		if prev_switch == False:
			def wait_for_keydown(SW_PREV):
                           while GPIO.input(SW_PREV):
                                 time.sleep(0.01)

                        def wait_for_keyup(SW_PREV):
                           while not GPIO.input(SW_PREV):
                                 time.sleep(0.01)
                        key_down_time = 0
                        key_down_leng = 0
                        while True:
                                 wait_for_keydown(SW_PREV)
                                 key_down_time = time.time()
                                 wait_for_keyup(SW_PREV)
                                 key_down_length = time.time() - key_down_time
                                 if key_down_length > 0.6:
                                         print "seek"
                                         subprocess.call(['mpc', 'seek','-8'])
                                 else:
                                         print "prev"
                                         subprocess.call(['mpc', 'prev'])
                                 break
		elif next_switch == False:
			def wait_for_keydown(SW_NEXT):
 			   while GPIO.input(SW_NEXT):
       				 time.sleep(0.01)

			def wait_for_keyup(SW_NEXT):
   			   while not GPIO.input(SW_NEXT):
       				 time.sleep(0.01)
			key_down_time = 0
			key_down_leng = 0
			while True:
   				 wait_for_keydown(SW_NEXT)
   				 key_down_time = time.time()
  				 wait_for_keyup(SW_NEXT)
				 key_down_length = time.time() - key_down_time
   				 if key_down_length > 0.6:
       					 print "seek"
					 subprocess.call(['mpc', 'seek','+8'])
   				 else:
       					 print "next"
					 subprocess.call(['mpc', 'next'])
			         break
#                        break
		elif stop_switch == False:
			subprocess.call(['mpc', 'stop' ])
                	print "stop"
		elif play_switch == False:
                        subprocess.call(['mpc', 'toggle' ])
#                        print "play"
                elif shtdwn_switch == False:
			os.system("shutdown -hf now")
#			print "shutdown in progress : wait 20 sec before unplug"
		elif reb_switch == False:
			os.system("shutdown -rf now")
#			print "reboot"
		time.sleep(0.5)
	except KeyboardInterrupt:
		print "\nExit"
		GPIO.setwarnings(False)
		GPIO.cleanup()
		sys.exit(0)
# End of program
