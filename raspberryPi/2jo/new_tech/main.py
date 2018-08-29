import RPi.GPIO as GPIO
import time
import sense
import crush
GPIO.setmode(GPIO.BOARD)
auto_driving_switch = 18 #auto_driving_switch
new_tech_switch = 22 #new_tech_switch
GPIO.setup(auto_driving_switch , GPIO.IN)
GPIO.setup(new_tech_switch , GPIO.IN)

def main():
    clutchA = newT = allN = isClutchA = isNewT = isAllN = 0
    
    print ("main code start!")
    #new_tech()
    while True :
        judgeNum = sense.judge()
        if judgeNum == 1:
            if GPIO.input(auto_driving_switch)==1:
                clutchA += 1
                #sense.ClutchAlarm()
            elif GPIO.input(new_tech_switch)==1:
                newT += 1
                #crush.new_tech()
            else :
                allN += 1
                #sense.AllNormal()
            if clutch > 10:
                isClutchA = 1
                clutchA = newT = allN = isNewT = isAllN = 0
            elif newT > 10:
                isNewT = 1
                clutchA = newT = allN = isClutchA = isAllN = 0
            elif allN > 10:
                isAllN = 1
                clutchA = newT = allN = isClutchA = isNewT = 0
            else:
                if isClutchA == 1:
                    sense.ClutchAlarm()
                elif isNewT == 1:
                    crush.new_tech()
                else:
                    sense.AllNormal()
                    

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        destroy()

