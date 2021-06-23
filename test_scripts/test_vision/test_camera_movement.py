import numpy as np
import cv2
import time
from rpi_ws281x import PixelStrip, Color

#LED strip configuration:
LED_COUNT = 20        # Number of LED pixels.
LED_PIN = 12          # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, range_led, wait_ms=50):
     """Wipe color across display a pixel at a time."""
     for i in range(range_led[0],range_led[1]):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)

if __name__ == '__main__':
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()
    colorWipe(strip, Color(255, 255, 255), (0,20))
    
    cap = cv2.VideoCapture(0+cv2.CAP_ANY)
    fgbg = cv2.createBackgroundSubtractorMOG2()

    while True:
        ret, frame = cap.read()
        fgmask = fgbg.apply(frame)

        percentage = (fgmask> 0).mean()
        if percentage > 0.01:
            time_start = time.time()
            start = 0
            print(percentage)
        else:
            time_now = time.time()
            if start == 0:
                time_start = time.time()
                start = 1
            if (time_now-time_start)>5:
                print('True')

        if cv2.waitKey(1) & 0xFF == ord('q'):
            colorWipe(strip, Color(0, 0, 0), (0,20), 10)
            break
    

cap.release()
cv2.destroyAllWindows()