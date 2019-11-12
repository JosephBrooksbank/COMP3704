from roku import Roku
import RPi.GPIO as GPIO
import time


PIN1 = 18
PIN2 = 23
PIN3 = 24
PIN4 = 25

# Connecting to Roku
roku = 0
rList = Roku.discover()
for r in rList:
    # On my personal network there are two Roku devices listed by the SSDP crawl; One of them is the remote
    # the remote uses port 80, so we can filter it out with nothing more than the port here.
    if r.port == 8060:
        roku = r
if roku == 0:
    raise Exception('No valid Rokus found on network')


GPIO.setmode(GPIO.BCM)
# Buttons setup, using an internal pull up resistor to simplify the physical circuit I have to build
GPIO.setup(PIN1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN4, GPIO.IN, pull_up_down=GPIO.PUD_UP)


while True:
    button1 = GPIO.input(PIN1)
    button2 = GPIO.input(PIN2)
    button3 = GPIO.input(PIN3)
    button4 = GPIO.input(PIN4)

    if button1 == False:
        print('Button 1 Pressed')
        roku.power()
        time.sleep(0.2)

    if button2 == False:
        print('Button 2 Pressed')
        roku.play()
        time.sleep(0.2)

    if button3 == False:
        print('Button 3 Pressed')
        roku.left()
        time.sleep(0.2)
    if button4 == False:
        print('Button 4 Pressed')
        roku.right()
        time.sleep(0.2)

