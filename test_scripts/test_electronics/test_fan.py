from gpiozero import PWMOutputDevice
from gpiozero import Button
from gpiozero.tones import Tone
import time

b = PWMOutputDevice(12)

button1 = Button(17)
button2 = Button(27)
button3 = Button(22)

while True:
    if button1.is_active:
        b.on()
        print("0")
    elif button2.is_active:
        b.toggle()
        print("1")
    elif button3.is_active:
        b.off()
        print("2")
    else:
        b.off()
        print('3')
    time.sleep(0.01)