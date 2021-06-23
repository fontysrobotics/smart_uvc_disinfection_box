from gpiozero import PWMOutputDevice,TonalBuzzer
from gpiozero import Button
from gpiozero.tones import Tone
import time

b = TonalBuzzer(13)

button1 = Button(27)
button2 = Button(22)
while True:
    if button1.is_active:
        
        b.play(Tone("C4"))
        print("pressed")
    elif button2.is_active:
        b.play(Tone("B4"))

    else:
        
        b.stop()
    time.sleep(0.01)