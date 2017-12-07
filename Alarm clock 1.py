import datetime
import time
import pyglet

Alarm_On = True

Alarm_Hour = 6
Alarm_Minute = 45
Alarm = datetime.time(Alarm_Hour,Alarm_Minute)


# States
# 0 - Display Off, 1 - Display On, 2 - Review Alarm, 3 - Edit Alarm
State = 0


def Read_Out (Disp):
    if (Disp==0):
        print ("Blank")
    elif(Disp==1) :
        print ("Time")
    elif(Disp==2) :
        print (Alarm_HMS)
    elif (Disp == 3):
        print(Alarm_Hour)
    elif (Disp == 4):
        print(Alarm_Minute)
    elif (Disp == 10) :
        print (Alarm_On)


Current_Time = datetime.datetime.now()
Current_Time_HMS = datetime.datetime.time(Current_Time)

tdelta = datetime.timedelta(seconds=3)
Alarm = Current_Time + tdelta
Alarm_HMS = datetime.datetime.time(Alarm)

Alarm_Test = Current_Time_HMS < Alarm_HMS
print (Current_Time_HMS)

window = pyglet.window.Window(width=100, height=100)

@window.event
Last_check = datetime.datetime.now()
if(key==pyglet.window.key.UP):
    if abs(Last_check-datetime.datetime.now()) < datetime.timedelta(seconds=1):
         Alarm_On = False
        print ("Change")
     Last_check = datetime.datetime.now()
    Read_Out(10)
elif(key==pyglet.window.key.LEFT):
            print("LEFT")
elif (key==pyglet.window.key.RIGHT):
            Read_Out(2)
pyglet.app.run()

while Alarm_On:

    while Alarm_Test:
        time.sleep(1)

        Current_Time = datetime.datetime.now()
        Current_Time_HMS = datetime.datetime.time(Current_Time)
        Alarm_Test = Current_Time_HMS < Alarm_HMS
        print (Alarm_HMS, ":", Current_Time_HMS)
    Alarm_On = False
print ("Alarm Off")



