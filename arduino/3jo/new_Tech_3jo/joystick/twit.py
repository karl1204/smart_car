#!/usr/bin/env python

# A basic Python Raspberry Pi project with twitter API integration and GPIO usage
# it requires that you have a Pi camera installed and enabled

# Written by Mike Haldas
# Detailed documentation and wiring instruction here: http://www.cctvcamerapros.com/Pi-Alarm-MMS
# Email me at mike@cctvcamerapros.net if yo                                                                     
                                                                     
                                                                     
                                             
#!/usr/bin/env python

# A basic Python Raspberry Pi project with twitter API integration and GPIO usage
# it requires that you have a Pi camera installed and enabled

# Written by Mike Haldas
# Detailed documentation and wiring instruction here: http://www.cctvcamerapros.com/Pi-Alarm-MMS
# Email me at mike@cctvcamerapros.net if you have questions
# You can also reach me @haldas on twitter or +Mike Haldas on Google+
# If you make any improvements to this code or use it in a cool way, please let me know

import time
import subprocess
import cv2
import RPi.GPIO as GPIO
from twython import Twython

#setup GPIO using Broadcom SOC channel numbering
GPIO.setmode(GPIO.BCM)
BUTTON = 24 
SYSTEM_READY = 25 # indicates that program is ready to be run
SYSTEM_RUNNING = 23 # indicates that program is running

GPIO.setup(SYSTEM_READY, GPIO.OUT) 
GPIO.setup(SYSTEM_RUNNING, GPIO.OUT) 
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

img = cv2.VideoCapture(0);
IMG_WIDTH = "1280"
IMG_HEIGHT = "720"
IMG_NAME = "tweet-pic.jpg"

# your twitter app keys goes here
apiKey = 'sVRtTTKDh7lrm72Z5IK74g7jx' # put twitter API Key here
apiSecret = 'wW7XnxlMYCW3zh0nuiZ81yC1GM1B7XveHHbzbUplziNIQiUMuK' # put twitter API Secret here
accessToken = '1023246194883973121-Pepn8fOVP9XJaPyVQASMPwlxvsZpND' # twitter access token here
accessTokenSecret = 'V35R5fLADIwWb1ZYd5uKkr4UZGe6Ct0I7Rpq6uVi1tMuO' # twitter access token secret

# this is the command to capture the image using pi camera
snapCommand = "raspistill -w " + IMG_WIDTH +  " -h " + IMG_HEIGHT + " -o " + IMG_NAME

api = Twython(apiKey,apiSecret,accessToken,accessTokenSecret)

GPIO.output(SYSTEM_READY, True) # set ready LED to on
GPIO.output(SYSTEM_RUNNING, False) # working LED to off
print("System Ready - push button to take picture and tweet.\n")




try:
	while True:

		GPIO.wait_for_edge(BUTTON, GPIO.RISING)
		##GPIO.input(BUTTON,True)

		print("Program running...\n")
		GPIO.output(SYSTEM_READY, False) # signal program not ready
		GPIO.output(SYSTEM_RUNNING, True) 

		print("Capturing photo...\n")
		ret = subprocess.call(snapCommand, shell=True)
		photo = open('/home/pi/smart_car/arduino/joystick/joystick_savingmovement_2servo/photo/tweet-pic.jpg', 'rb')

		print("Uploading photo to twitter...\n")
		media_status = api.upload_media(media=photo)

		time_now = time.strftime("%H:%M:%S") # get current time
		date_now =  time.strftime("%d/%m/%Y") # get current date
		tweet_txt = "Photo captured by @twybot at " + time_now + " on " + date_now

		print("Posting tweet with picture...\n")
		api.update_status(media_ids=[media_status['media_id']], status=tweet_txt)

		#deprecated method replaced by upload_media() and update_status()
		#api.update_status_with_media(media=photo, status=tweetStr)

		GPIO.output(SYSTEM_RUNNING, False) 
		GPIO.output(SYSTEM_READY, True) # signal program ready
		print("Done - System ready again.\n")
		
		#cv2.imshow('screen',img)

except KeyboardInterrupt:
	GPIO.output(SYSTEM_READY_LED,False)
	GPIO.cleanup()

finally:
    GPIO.cleanup()