import cv2
import imutils
import numpy as np
import matplotlib.pyplot as plt

class contours():
    def __init__(self):
        self.image = cv2.imread("objects_0.jpg")

    def filters(self):
        image_blur = cv2.medianBlur(self.image,25)
        image_blur = cv2.GaussianBlur(image_blur,(5, 5), 0)
        image_blur_gray = cv2.cvtColor(image_blur, cv2.COLOR_BGR2GRAY)
        __ ,image_thresh = cv2.threshold(image_blur_gray,220,255,cv2.THRESH_BINARY_INV)

        kernel = np.ones((17,17),np.uint8)
        self.opening = cv2.morphologyEx(image_thresh,cv2.MORPH_CLOSE,kernel) 

    def contours(self):
        self.cnts = cv2.findContours(self.opening.copy(), cv2.RETR_EXTERNAL,
	        cv2.CHAIN_APPROX_SIMPLE)
        self.cnts = imutils.grab_contours(self.cnts)

    def display(self,cmap="gray"):
        f_image = cv2.imread("objects_0.jpg")
        f, axs = plt.subplots(1,2,figsize=(12,5))
        axs[0].imshow(f_image,cmap="gray")
        axs[1].imshow(self.image,cmap="gray")
        axs[1].set_title("Total Objects = {}".format(len(self.cnts)))
    
        for (i, c) in enumerate(self.cnts):
            ((x, y), _) = cv2.minEnclosingCircle(c)
            cv2.putText(self.image, "#{}".format(i + 1), (int(x) - 45, int(y)+20),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
            cv2.drawContours(self.image, [c], -1, (0, 255, 0), 2)

    def show_image(self):
        cv2.imshow('final', self.image)
        cv2.waitKey()
        cv2.destroyAllWindows()
        
if __name__ == '__main__':
    contours = contours()
    contours.filters()
    contours.contours()
    contours.display()
    contours.show_image()