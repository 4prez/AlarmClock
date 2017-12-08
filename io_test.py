from time import sleep
import RPi.GPIO as GPIO
## import uinput as ui
import datetime as dt

GPIO.setmode(GPIO.BOARD)
B_L=16
R_R=12
GPIO.setup(B_L,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(R_R,GPIO.IN,pull_up_down=GPIO.PUD_UP)

B_L_Status = 1
R_R_Status = 1

while True:
	if GPIO.input(B_L)!=B_L_Status:
		if GPIO.input(B_L)==0:
			B_L_PressTime = dt.datetime.now()
		else:
			B_L_Duration = dt.datetime.now()-B_L_PressTime
			Key_Press = "L"
			print ("L")
			if B_L_Duration > dt.timedelta(seconds=1):
				New_Input="Long"
			else:
				New_Input="Short"
			print (New_Input)
	if GPIO.input(R_R)!=R_R_Status:
		if GPIO.input(R_R)==0:
			R_R_PressTime = dt.datetime.now()
		else:
			R_R_Duration = dt.datetime.now() - R_R_PressTime
			Key_Press = "R"
			print ("R")
			if R_R_Duration > dt.timedelta(seconds=1):
				New_Input = "Long"
			else:
				New_Input = "Short"
			print (New_Input)
	B_L_Status = GPIO.input(B_L)
	R_R_Status = GPIO.input(R_R)
	sleep(.1)

	

