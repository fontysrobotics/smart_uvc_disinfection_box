from gpiozero import Button
import time

button = Button(16)
while True:
    if button.is_active:
        print(button.is_active)
    else:
        print(button.is_active)
    time.sleep(0.01)