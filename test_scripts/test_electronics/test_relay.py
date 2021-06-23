from gpiozero import DigitalOutputDevice 
from gpiozero import Button
import time 
#GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
 
RELAIS_1_GPIO = DigitalOutputDevice(25)
RELAIS_2_GPIO = DigitalOutputDevice(8)

button0 = Button(17)
button1 = Button(27)
button2 = Button(22)
while True:
    if button1.is_active:
        print("pressed")
        RELAIS_1_GPIO.on()
    elif button2.is_active:
        print("not pressed")
        RELAIS_2_GPIO.on()
    elif button0.is_active:
        RELAIS_1_GPIO.on()
        RELAIS_2_GPIO.on()
    else:
       RELAIS_1_GPIO.off()
       RELAIS_2_GPIO.off()
    time.sleep(0.01)