#!/usr/bin/python
#
# Copy to /usr/local/bin
#

import RPi.GPIO as GPIO
import time

# The pin on the Raspberry Pi P1 header that resets your Arduino
pin = 4

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)

print "Resetting AVR"
GPIO.output(pin, GPIO.LOW)
time.sleep(1)
GPIO.output(pin, GPIO.HIGH)
GPIO.cleanup()
