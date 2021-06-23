import numpy as np
import cv2 as cv

cap = cv.VideoCapture(2, cv.CAP_ANY)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow('frame', gray)
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()

# def testDevice(source):
#    cap = cv.VideoCapture(source) 
#    if cap is None or not cap.isOpened():
#        print('Warning: unable to open video source: ', source)

# for i in range(-10,10):
#     testDevice(i) 