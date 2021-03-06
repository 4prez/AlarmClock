import datetime as dt
from pygame import *
from time import sleep
# from os import environ
import os
import sys

# Check if running on Pi (linux) vs windows (for development)
On_Raspberry = not (sys.platform == 'win32') # determine if running on Windows or Pi (for inputs)
print("Running on Raspberry:",On_Raspberry)

init()
# set SDL to use the dummy NULL video driver, so it doesn't need a windowing system.
os.environ["SDL_VIDEODRIVER"] = "dummy"
screen = display.set_mode((160, 160))

print ("Pygame window initialized")

# Default Alarm Setting
Alarm_On = False
Alarm_Hour = 6
Alarm_Minute = 30
Alarm_Minute_Increment = 5  # how much the Alarm_Minute increase with each button press
Alarm_HMS = dt.time(Alarm_Hour, Alarm_Minute, 0)
Alarm_Sound = 1
Alarm_Volume = 3
Alarm_Playing = False
Alarm_Sample = False
Alarm_Duration = 1  # how long the Alarm will run before shutting itself off

# Default Soundbox settings
SBox_Sound = 1
SBox_Volume = 3
SBox_Duration = 2
SBox_Duration_List = [5, 10, 20, 30, 45, 60, 120, 240]
SBox_Start_Time = dt.datetime.now()
SBox_End_Time = SBox_Start_Time + dt.timedelta(minutes=SBox_Duration)
SBox_Playing = False
Fade_Out_ms = 1000  # In milliseconds

# Initiate key press variables / flags
New_Input = False
Key_Press = "None"
Key_TimeStamp = dt.datetime.now()
Key_Down_Stamp = dt.datetime(1970, 1, 1, 0, 0, 0, 0)
TimeStamp_Check = dt.timedelta(seconds=10)  # inactive time for menu level reversion

# Sound files
# List of sound files (same for Alarm and Soundbox), need to be in the same directory as py file
# https://www.youtube.com/watch?v=C-t0nZ_8HeE

Sound_List =[]
SoundBox_Path = (os.path.join(os.getcwd(),"Soundbox Sounds"))
for files in os.listdir(SoundBox_Path):
    if files.endswith(".mp3"):
        # print(files)
        Sound_List.append(files)
print(Sound_List)
print ("SoundBox files loaded:",len(Sound_List))

Alarm_List =[]
Alarm_Path = (os.path.join(os.getcwd(),"Alarm Sounds"))
for files in os.listdir(Alarm_Path):
    if files.endswith(".mp3"):
        # print(files)
        Alarm_List.append(files)
print(Alarm_List)
print("Alarm files loaded:",len(Alarm_List))

## Setup GPIO for Raspberry - buttons, display
if On_Raspberry:

    ## Buttons
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)
    B_L = 13
    R_R = 11
    GPIO.setup(B_L, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(R_R, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    B_L_Status = 1
    R_R_Status = 1

    def callback_button(inputpin):
        # define global variable to allow the passing of data
        global Key_Down_Stamp, New_Input, Key_Press, Menu_Revert_Time, TimeStamp_Check
        if GPIO.input(inputpin) == 1:
            New_Input = True
            if inputpin == B_L:
                Key_Press = "L"
            elif inputpin == R_R:
                Key_Press = "R"

            if (dt.datetime.now() - Key_Down_Stamp) > dt.timedelta(seconds=1):
                New_Input = "Long"
            else:
                New_Input = "Short"
            Menu_Revert_Time = dt.datetime.now() + TimeStamp_Check
        else:
            Key_Down_Stamp = dt.datetime.now()

    GPIO.add_event_detect(B_L, GPIO.BOTH, callback=callback_button)
    GPIO.add_event_detect(R_R, GPIO.BOTH, callback=callback_button)

    ## SevenSegment Display
    from Adafruit_LED_Backpack import SevenSegment
    ssdisplay = SevenSegment.SevenSegment()
    ssdisplay.begin()
    ssdisplay.clear()
    ssdisplay.write_display()
    print("SevenSegment Display Initiated")

    ## LED wake

    ## Distance

    ## Light Sensor


print("Raspberry GPIO setup as required")

## Special print function for SevenSegment
def DispPrint(disptext,lt_coln = False,rt_coln = True):
    global On_Raspberry, Alarm_On
    print("Display:", disptext,lt_coln, rt_coln, Alarm_On)
    if On_Raspberry:
        if type(disptext).__name__ == 'list':
            for i in range (0,len(disptext)):
                ssdisplay.set_digit(i, disptext[i])
        elif type(disptext).__name__ == 'float':
            ssdisplay.print_float(disptext)
        elif type(disptext).__name__ == 'bool':
            for i in range (0,4):
                ssdisplay.set_digit(i, int(disptext[i]))
        elif disptext == 'now':
            ssdisplay.print_float(float(dt.datetime.now().strftime('%H.%M')))
            print("imbedded now")
            # print(dt.datetime.now().strftime('%H:%M'))
            rt_coln = True
            lt_coln = False
        else:
            ssdisplay.clear()
            print("else-blank")
        # ssdisplay.set_right_colon(rt_coln)
        # ssdisplay.set_left_colon(lt_coln)
        # ssdisplay.writeDigitRaw(2, 0x02) #rt colon
        # ssdisplay.writeDigitRaw(2, 0x08) # upper left colon
        # ssdisplay.writeDigitRaw(2, 0x04) # lower left colon
        ssdisplay.set_fixed_decimal(Alarm_On)
        ssdisplay.write_display()

## Initiate main loop
Exit_Now = False
State = 0

DispPrint("blank")

while not Exit_Now:
    ## pygame event loop to capture inputs
    if On_Raspberry == False:
        for e in event.get():
            ## Log the key that was pressed
            if e.type == KEYDOWN:
                Key_Down_Stamp = dt.datetime.now()
                # print(Key_Down_Stamp)
                if (e.key == K_UP):
                    # print ("U")
                    Key_Press = "U"
                    Exit_Now = True
                elif (e.key == K_LEFT):
                    Key_Press = "L"
                # print("L")
                elif (e.key == K_RIGHT):
                    Key_Press = "R"
                # print("R")

            ## Determine if it is a short or long press
            if e.type == KEYUP:
                if (dt.datetime.now() - Key_Down_Stamp) > dt.timedelta(seconds=1):
                    New_Input = "Long"
                else:
                    New_Input = "Short"

                Menu_Revert_Time = dt.datetime.now() + TimeStamp_Check

    ## Calculate the Alarm time
    if dt.time(Alarm_Hour, Alarm_Minute, 0).strftime('%H:%M') < dt.datetime.now().strftime('%H:%M'):
        Alarm_Date_Offest = dt.timedelta(days=1)
    else:
        Alarm_Date_Offest = dt.timedelta(days=0)
    Current_Time = dt.datetime.now()
    Alarm_DateTime = dt.datetime(Current_Time.year, Current_Time.month, Current_Time.day, Alarm_Hour,
                                       Alarm_Minute, 0) + Alarm_Date_Offest
    Alarm_HMS = Alarm_DateTime.strftime('%H:%M')

    ## Stop sounds
    if (Alarm_Playing == True and \
        (New_Input != False or dt.datetime.now() > Alarm_End_Time)) or \
            (SBox_Playing == True and \
             ((New_Input == "Long" and Key_Press == "L") or \
              dt.datetime.now() > SBox_End_Time)):
        mixer.music.fadeout(Fade_Out_ms)
        SBox_Playing = False
        if Alarm_Playing == True:
            Alarm_Playing = False
            Alarm_On = False
        New_Input = False
        print("Sound Off")
        print(dt.datetime.now().strftime('%H:%M'))
        DispPrint("now")
        State = 1

    ## With inactive time the menu reverts
    if (State > 0 and dt.datetime.now() > Menu_Revert_Time):
        if State == 1:
            State = 0
            DispPrint("blank")
        elif State >1: #(State > 10 or State == 6): # For old revert ladder
            State = 1
            DispPrint("now")
            # print(dt.datetime.now().strftime('%H:%M'))
            Menu_Revert_Time = dt.datetime.now() + TimeStamp_Check
        # elif State > 1:  # For old revert ladder
        #     Key_Press = "L"
        #     # print("L-Delay")
        #     Menu_Revert_Time = dt.datetime.now() + TimeStamp_Check
        #     State = State - 2
        #     New_Input = "Short"

    ## Long key escape actions
    if New_Input == "Long":
        if Key_Press == "L":
            if State > 4 and State < 10:
                mixer.music.load(os.path.join(Alarm_Path,Alarm_List[Alarm_Sound - 1]))
                mixer.music.set_volume(Alarm_Volume / 5.)
                mixer.music.play(-1)
                Alarm_Sample = True
            elif State < 2:
                Menu_Revert_Time = Menu_Revert_Time + dt.timedelta(seconds=10)
                State = 11
                if SBox_Playing:
                    mixer.music.stop()
                else:
                    mixer.music.load(os.path.join(SoundBox_Path,Sound_List[SBox_Sound - 1]))
                    mixer.music.set_volume(SBox_Volume / 5.)
                    mixer.music.play(-1)
                    SBox_Playing = True
                    SBox_Start_Time = dt.datetime.now()
                    SBox_End_Time = SBox_Start_Time + dt.timedelta(minutes=SBox_Duration)
                    print("Soundbox sound", SBox_Sound)
                    DispPrint([int(SBox_Sound / 10), SBox_Sound % 10, None, None], lt_coln=True, rt_coln=False)

        elif Key_Press == "R":
            Exit_Now = True

    ## Step through the Menus
    if New_Input == "Short":
        if State == 0:  # Display is off
            State = 1
            # print(dt.datetime.now().strftime('%H:%M'))
            DispPrint("now")
        elif State == 1:  # Time is on
            if Alarm_On == False:
                print("Alarm is", Alarm_On)
                DispPrint([int(Alarm_On), int(Alarm_On), int(Alarm_On), int(Alarm_On)], rt_coln=False, lt_coln=True)
            elif Alarm_On == True:
                print("Alarm time", Alarm_HMS)
                DispPrint(Alarm_Hour+Alarm_Minute/100,lt_coln=True,rt_coln=True)
            State = 2

        elif State == 2:  # Toggle Alarm On/Off
            if Key_Press == "R":
                Alarm_On = not Alarm_On
                print("Alarm is", Alarm_On)
                DispPrint([int(Alarm_On),int(Alarm_On),int(Alarm_On),int(Alarm_On)],rt_coln=False,lt_coln=True)

            elif Key_Press == "L":
                if Alarm_On == True:
                    DispPrint([int(Alarm_Hour / 10),Alarm_Hour % 10, None,None] )
                    State = 3
                else:
                    print("Alarm is", Alarm_On)
                    DispPrint("now")
                    State = 1

        elif State == 3:  # Edit Hour
            if Key_Press == "R":
                if Alarm_Hour == 23:
                    Alarm_Hour = 0
                else:
                    Alarm_Hour = Alarm_Hour + 1
                DispPrint([int(Alarm_Hour / 10), Alarm_Hour % 10, None, None],rt_coln=True)
                # print("Alarm hour", Alarm_Hour)
            elif Key_Press == "L":
                State = 4
                # print(State)
                # print("Alarm minute", Alarm_Minute)
                DispPrint([None, None,int(Alarm_Minute / 10), Alarm_Minute % 10],rt_coln=True)


        elif State == 4:  # Edit Minute
            if Key_Press == "R":
                if Alarm_Minute > 59 - Alarm_Minute_Increment:
                    Alarm_Minute = 0
                else:
                    Alarm_Minute = Alarm_Minute + Alarm_Minute_Increment
                DispPrint([None, None, int(Alarm_Minute / 10), Alarm_Minute % 10],rt_coln=True)
                # print("Alarm minute", Alarm_Minute)
            elif Key_Press == "L":
                State = 5
                # print(State)
                print("Alarm sound", Alarm_Sound)
                DispPrint([int(Alarm_Sound / 10), Alarm_Sound % 10, None, None],rt_coln=False,lt_coln=True)
                if Alarm_Sample:
                    mixer.music.fadeout(Fade_Out_ms)


        elif State == 5:  # Edit Sound
            if Key_Press == "R":
                if Alarm_Sound == len(Alarm_List):
                    Alarm_Sound = 1
                else:
                    Alarm_Sound = Alarm_Sound + 1
                if Alarm_Sample:
                    mixer.music.load(Alarm_List[Alarm_Sound - 1])
                    mixer.music.set_volume(Alarm_Volume / 5.)
                    mixer.music.play(-1)
                print("Alarm sound", Alarm_Sound)
                DispPrint([int(Alarm_Sound / 10), Alarm_Sound % 10, None, None], rt_coln=False, lt_coln=True)
            elif Key_Press == "L":
                State = 6
                # print(State)
                print("Alarm volume", Alarm_Volume, "of 5")
                DispPrint([None, None,Alarm_Volume,None], rt_coln=False, lt_coln=True)

        elif State == 6:  # Edit volume
            if Key_Press == "R":
                if Alarm_Volume == 5:
                    Alarm_Volume = 1
                else:
                    Alarm_Volume = Alarm_Volume + 1
                if Alarm_Sample:
                    mixer.music.pause()
                    mixer.music.set_volume(Alarm_Volume / 5.)
                    mixer.music.unpause()
                print("Alarm volume", Alarm_Volume, "of 5")
                DispPrint([None, None, Alarm_Volume, None], lt_coln=True, rt_coln=False)
            elif Key_Press == "L":
                State = 1
                # print(State)
                print("Alarm is", Alarm_On)
                print("Alarm time", Alarm_HMS)
                print("Alarm sound", Alarm_Sound)
                print("Alarm volume is", Alarm_Volume, "of 5")
                DispPrint(Alarm_Hour+Alarm_Minute/100, lt_coln=True, rt_coln=True)
                if Alarm_Sample:
                    mixer.music.fadeout(Fade_Out_ms)

        elif State == 11:  # Soundbox Sound
            if Key_Press == "R":
                if SBox_Sound == len(Sound_List):
                    SBox_Sound = 1
                else:
                    SBox_Sound = SBox_Sound + 1
                print("Soundbox sound", SBox_Sound)
                DispPrint([int(SBox_Sound / 10), SBox_Sound % 10, None, None], rt_coln=False, lt_coln=True)
                mixer.music.load(os.path.join(SoundBox_Path, Sound_List[SBox_Sound - 1]))
                mixer.music.set_volume(SBox_Volume / 5.)
                mixer.music.play(-1)
                SBox_Start_Time = dt.datetime.now()
                SBox_End_Time = SBox_Start_Time + dt.timedelta(minutes=SBox_Duration)
            elif Key_Press == "L":
                State = 12
                # print(State)
                print("Soundbox volume", SBox_Volume, "of 5")
                DispPrint([None, None, SBox_Volume, None], rt_coln=False, lt_coln=True)

        elif State == 12:  # Soundbox Volume
            if Key_Press == "R":
                if SBox_Volume == 5:
                    SBox_Volume = 1
                else:
                    SBox_Volume = SBox_Volume + 1
                mixer.music.pause()  # pause/unpoause prevents popping when dropping to low volume
                mixer.music.set_volume(SBox_Volume / 5.)
                mixer.music.unpause()
                print("Soundbox volume", SBox_Volume, "of 5")
                DispPrint([None, None, SBox_Volume, None], rt_coln=False, lt_coln=True)
            elif Key_Press == "L":
                State = 13
                # print(State)
                print("Soundbox duration is", SBox_Duration_List[SBox_Duration], "min")
                sbd = SBox_Duration_List[SBox_Duration]
                sbd_h = int(sbd/60)
                sbd_m = sbd - sbd_h*60
                sbd_hm = float(sbd_h+sbd_m/100)
                DispPrint(sbd_hm, rt_coln=True)

        elif State == 13:  # Soundbox Duration
            if Key_Press == "R":
                if SBox_Duration > len(SBox_Duration_List) - 2:
                    SBox_Duration = 0
                else:
                    SBox_Duration = SBox_Duration + 1
                print("Soundbox duration is", SBox_Duration_List[SBox_Duration], "min")
                sbd = SBox_Duration_List[SBox_Duration]
                sbd_h = int(sbd / 60)
                sbd_m = sbd - sbd_h * 60
                sbd_hm = float(sbd_h + sbd_m / 100)
                DispPrint(sbd_hm, rt_coln=True)
                SBox_End_Time = SBox_Start_Time + dt.timedelta(minutes=SBox_Duration_List[SBox_Duration])
            elif Key_Press == "L":
                State = 11
                print("Soundbox sound", SBox_Sound)
                DispPrint([int(SBox_Sound / 10), SBox_Sound % 10, None, None], rt_coln=False, lt_coln=True)

    New_Input = False

    if Alarm_On:
        if not Alarm_Playing:
            if dt.datetime.now() > Alarm_DateTime:
                print("Alarm Playing")
                mixer.music.load(os.path.join(Alarm_Path, Alarm_List[Alarm_Sound - 1]))
                mixer.music.set_volume(0)
                mixer.music.play(-1)
                Alarm_Start_Time = dt.datetime.now()
                Alarm_End_Time = Alarm_Start_Time + dt.timedelta(minutes=Alarm_Duration)
                Alarm_Playing = True
        else:  # Volume Fade In
            mixer.music.set_volume(min(Alarm_Volume / 5.0, (dt.datetime.now() - Alarm_Start_Time).seconds / 10.))

    if On_Raspberry == True:  ## For button capture
        B_L_Status = GPIO.input(B_L)
        R_R_Status = GPIO.input(R_R)

mixer.music.load(os.path.join(SoundBox_Path,Sound_List[0]))
mixer.music.play(1)
sleep(1)

if On_Raspberry == True:
    GPIO.cleanup()
    ssdisplay.clear()
    ssdisplay.write_display()
