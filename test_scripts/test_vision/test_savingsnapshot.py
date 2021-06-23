import cv2
cam = cv2.VideoCapture(0, cv2.CAP_ANY)
ret, frame = cam.read()

if ret:
    name = 'scans/objects_{}.jpg'.format(0)
    cv2.imwrite(name, frame)

cam.release()
cv2.destroyAllWindows()