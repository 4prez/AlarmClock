from time import sleep
import RPi.GPIO as GPIO
## import uinput as ui
import datetime as dt

GPIO.setmode(GPIO.BOARD)
B_L = 16
R_R = 12
GPIO.setup(B_L, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(R_R, GPIO.IN, pull_up_down=GPIO.PUD_UP)

B_L_Status = 1
R_R_Status = 1

New_Input = False


def callback_button(inputpin):
    if GPIO.input(input) == 0:
        Key_Down_Stamp = dt.datetime.now()
    else:
        New_Input = True

        if inputpin == B_L:
            Key_Press = "L"
        elif inputpin == R_R:
            Key_Press = "R"

        if (datetime.datetime.now() - Key_Down_Stamp) > datetime.timedelta(seconds=1):
            New_Input = "Long"
        else:
            New_Input = "Short"
        Menu_Revert_Time = datetime.datetime.now()  # + TimeStamp_Check


GPIO.add_event_detect(B_L, GPIO.BOTH, callback=callback_button)
GPIO.add_event_detect(R_R, GPIO.BOTH, callback=callback_button)

while True:
    if New_Input != False:
        print(Key_Press)
        print(New_Input)
        New_Input = False

GPIO.cleanup()
