import serial
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
pin = 11 #LED pin number
ser = serial.Serial("/dev/ttyACM0",115200)  # 두번째 인자값이 보레이트 설정

def crush():
    #set var

    while True :

        fire , heartpulse , sona , impact = sensing()
        if fire == -1 :
            continue

        while True :

            Accident = 0

            if fire >= 500 : ##fire signal is measured as analog, if it is over 500, then there are fire around sensor.
                print("Fire Fire Fire")
                Accident = 1

            if heartpulse >= 130 and heartpulse <=30 : ##normal heartpulse is between 49 ~ 90
                print("Driver is under heart attack")
                #if heart attack has been happend, Auto driving must be started!!
                Accident = 1

            if impact == 1 and ( sona <= 20 or sona >= 4000 ) : ##sona data occasionally measured as 2000~2500 without any reason.
                print("Car crush has been happened")
                Accident = 1


            if Accident == 1 : # if Accident happend,

                gpsx, gpsy = gps() # GPS signal is transmitted,

                ######################LED SOS SIGNAL######################
                for i in range(3) : # SOS 3 times
                    for i in range(3) : # signal 'S'
                        GPIO.output(pin,True)
                        time.sleep(0.5)
                        GPIO.output(pin,False)
                        time.sleep(1)
                    for i in range(3) : # signal 'O'
                        GPIO.output(pin,True)
                        time.sleep(3)
                        GPIO.output(pin,False)
                        time.sleep(1)
                    for i in range(3) : # signal 'S'
                        GPIO.output(pin,True)
                        time.sleep(0.5)
                        GPIO.output(pin,False)
                        time.sleep(1)

                GPIO.cleanup()
                break


def sensing():
    if ser.readable() :
        str_ard = ser.readline()

    else :
        return -1, -1, -1, -1
    return fire , heartpulse , sona , impact

