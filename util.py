import time
import cv2

def colorWipe(strip, color, range_led, wait_ms=10):
    """Wipe color across display a pixel at a time."""
    for i in range(range_led[0],range_led[1]):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)

def theaterChase(strip, color, range_led, wait_ms=250, iterations=2):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(range_led[0], range_led[1], 3):
                strip.setPixelColor(i + q, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(range_led[0], range_led[1], 3):
                strip.setPixelColor(i + q, 0)

def take_picture(camera_nr):
    cam = cv2.VideoCapture(camera_nr, cv2.CAP_ANY)
    ret, frame = cam.read()

    if ret:
        name = 'scans/objects_{}.jpg'.format(camera_nr)
        cv2.imwrite(name, frame)

    cam.release()
    cv2.destroyAllWindows()
    # return name