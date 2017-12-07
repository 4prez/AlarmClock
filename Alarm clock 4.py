import datetime
import time as tm
from pygame import *
import os, sys


init()
# set SDL to use the dummy NULL video driver,
#   so it doesn't need a windowing system.
os.environ["SDL_VIDEODRIVER"] = "dummy"
screen = display.set_mode((160,160))


# Main Loop Exit
Exit_Now = False

# Default Alarm Setting
Alarm_On = True
Alarm_Hour = 6
Alarm_Minute = 45
Alarm_HMS = datetime.time(Alarm_Hour, Alarm_Minute,0)

# Initiate key press variables / flags
New_Input = False
Key_Press = "None"
Key_TimeStamp = datetime.datetime.now()
TimeStamp_Check = datetime.timedelta(seconds=5)

# States
# 0 - Display Off, 1 - Display On, 2 - Review Alarm, 3 - Edit Alarm
State = 0
Stage2_RPass = False

# Current_Time = datetime.datetime.now()
# Current_Time_HMS = datetime.datetime.time(Current_Time)
# Alarm_Test = Current_Time_HMS < Alarm_HMS
# print (Current_Time_HMS)


# Initiate loop
while not Exit_Now:
    #pygame event loop
    for e in event.get():
        if e.type == KEYDOWN:
            if (e.key == K_UP):
                # print ("U")
                Key_Press = "U"
                New_Input = True
                Exit_Now = True
            elif (e.key == K_LEFT):
                Key_Press = "L"
                # print("L")
                New_Input = True
            elif (e.key == K_RIGHT):
                Key_Press = "R"
                # print("R")
                New_Input = True
            Key_TimeStamp = datetime.datetime.now() + TimeStamp_Check
            # print ("Key_TimeStamp ",Key_TimeStamp)



    Alarm_HMS = datetime.time(Alarm_Hour, Alarm_Minute,0).strftime('%H:%M')



    if (State >1 and datetime.datetime.now() > Key_TimeStamp):
        Key_Press = "L"
        # print("L-Delay")
        Key_TimeStamp = datetime.datetime.now() + TimeStamp_Check
        State = State - 2
        New_Input = True

    if New_Input == True:
        if Key_Press == "U":
            Exit_Now = True

        elif State == 0:
            # print (datetime.datetime.now())
            print(datetime.datetime.now().strftime('%H:%M'))
            State = 1
            # print (State)

        elif State == 1:
            print("Alarm is ", Alarm_On)
            if Alarm_On == True:
                print("Alarm is ", Alarm_HMS)
            State = 2
            # print(State)

        elif State == 2: # Base Time
            if Key_Press == "L":
                if Alarm_On == True:
                    if Stage2_RPass == True:
                        print("Alarm Hour", Alarm_Hour)
                        State = 3
                        # print(State)
                        Stage2_RPass = False
                    else:
                        print("Alarm is ", Alarm_On)
                        print("Alarm is ", Alarm_HMS)
                else:
                    print("Alarm is ", Alarm_On)
                    State = 1
                    # print(State)
            elif Key_Press == "R":
                Alarm_On = not Alarm_On
                print("Alarm is ", Alarm_On)
                Stage2_RPass = True

        elif State == 3: # Hour Edit
            if Key_Press == "L":
                State = 4
                # print(State)
                print("Alarm Minute", Alarm_Minute)
            elif Key_Press == "R":
                if Alarm_Hour == 23:
                    Alarm_Hour = 0
                else:
                    Alarm_Hour = Alarm_Hour + 1
                print("Alarm Hour", Alarm_Hour)

        elif State == 4:  # Hour Edit
            if Key_Press == "L":
                State = 1
                # print(State)
                print("Alarm is ", Alarm_On)
                print("Alarm is ", Alarm_HMS)
            elif Key_Press == "R":
                if Alarm_Minute == 55:
                    Alarm_Minute = 0
                else:
                    Alarm_Minute = Alarm_Minute + 5
                print("Alarm Minute", Alarm_Minute)
    New_Input = False

mixer.music.load("Rain_thunder.mp3")
mixer.music.play(1)
tm.sleep(10)

    # print("State: ", State, " DateTimeNow: ", datetime.datetime.now(), " Key_TimeStamp: ", Key_TimeStamp)

#    print(datetime.datetime.now())


  #  while Alarm_Test:
  #      time.sleep(1)

   #     Current_Time = datetime.datetime.now()
    #    Current_Time_HMS = datetime.datetime.time(Current_Time)
     #   Alarm_Test = Current_Time_HMS < Alarm_HMS
      #  print (Alarm_HMS, ":", Current_Time_HMS)
    #Alarm_On = False



#print ("Alarm Off")



