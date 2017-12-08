from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
B_L=16
R_R=12
GPIO.setup(B_L,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(R_R,GPIO.IN,pull_up_down=GPIO.PUD_UP)
while True:
	if GPIO.input(B_L)==0:
		print ("B_L was pressed")
		sleep(.1)
	if GPIO.input(R_R)==0:
		print ("R_R was pressed")
		sleep(.1)


