import datetime
import time
import pyglet


Alarm_On = True
Exit_Now = False
New_Input = False
Key_Press = "None"

Alarm_Hour = 6
Alarm_Minute = 45
Alarm = datetime.time(Alarm_Hour,Alarm_Minute)



# States
# 0 - Display Off, 1 - Display On, 2 - Review Alarm, 3 - Edit Alarm
State = 0

Current_Time = datetime.datetime.now()
Current_Time_HMS = datetime.datetime.time(Current_Time)

tdelta = datetime.timedelta(seconds=3)
Alarm = Current_Time + tdelta
Alarm_HMS = datetime.datetime.time(Alarm)

Alarm_Test = Current_Time_HMS < Alarm_HMS
print (Current_Time_HMS)


def key_pass(Key_Activated):
    Key_Press = Key_Activated
    return Key_Press

while not Exit_Now:

    window = pyglet.window.Window(width=100, height=100)

    @window.event
    def on_key_press(key,modifiers):
        if (key == pyglet.window.key.UP):
            key_pass("U")
            print ("U")
            Key_Press = "U"
            return Key_Press
            pyglet.app.exit()
        elif (key == pyglet.window.key.LEFT):
            key_pass("L")
            print("L")
            pyglet.app.exit()
        elif (key == pyglet.window.key.RIGHT):
            key_pass("R")
            print("R")
            pyglet.app.exit()
    pyglet.app.run()


    if New_Input == True:
        if Key_Press == "U":
            Exit_Now = True

        elif State == 0:
            State = 1
            New_Input = False

        elif State == 1: # Base Time
            if Key_Pressress == "L":
                print ("Alarm is ",Alarm_On)
                print ("Alarm is ",Alarm_HMS)
            elif Key_Press == "R":
                Alarm_On = not Alarm_On
                print("Alarm is ", Alarm_On)
                if Alarm_On == True:
                    print("Alarm is ", Alarm_HMS)
                State = 2

        elif State == 2: # Hour Edit
            if Key_Press == "L":
                State = 3
                print("Alarm Minute", Alarm_Minute)
            elif Key_Press == "R":
                Alarm_Hour = Alarm_Hour + 1
                print("Alarm Hour", Alarm_Hour)

        elif State == 3:  # Hour Edit
            if Key_Press == "L":
                State = 1
                print("Alarm is ", Alarm_HMS)
            elif Key_Press == "R":
                Alarm_Minute = Alarm_Minute + 5
                print("Alarm Minute", Alarm_Minute)




  #  while Alarm_Test:
  #      time.sleep(1)

   #     Current_Time = datetime.datetime.now()
    #    Current_Time_HMS = datetime.datetime.time(Current_Time)
     #   Alarm_Test = Current_Time_HMS < Alarm_HMS
      #  print (Alarm_HMS, ":", Current_Time_HMS)
    #Alarm_On = False



#print ("Alarm Off")



