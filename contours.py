import cv2
import imutils
import numpy as np

class contours():
    def __init__(self, name_image):
        self.image = cv2.imread(name_image)
        self.area_list = []
        self.index_to_remove = []
        self.total_area = 0

    def filters(self):
        # Function for filtering image
        image_blur = cv2.medianBlur(self.image,25)
        image_blur = cv2.GaussianBlur(image_blur,(5, 5), 0)
        image_blur_gray = cv2.cvtColor(image_blur, cv2.COLOR_BGR2GRAY)
        __ ,image_thresh = cv2.threshold(image_blur_gray,220,255,cv2.THRESH_BINARY_INV)

        kernel = np.ones((17,17),np.uint8)
        self.opening = cv2.morphologyEx(image_thresh,cv2.MORPH_CLOSE,kernel) 

    def contours(self):
        # Find the contours in the filtered image. Only find the outer contours and approximate the outer edges. 
        # Then calculate the areas of all the contous. Then remove all the small contours.
        self.contour = cv2.findContours(self.opening.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.contour = imutils.grab_contours(self.contour)
        self.calculated_areas_of_contours()
        self.remove_small_contours()

    def calculated_areas_of_contours(self):
        # Calculate for alle the found contours the area in square mm.
        for i, j in enumerate(self.contour):
            pixels = int(cv2.contourArea(self.contour[i]))
            area = pixels / 9.85  # square mm
            
            self.area_list.append(area)

    def remove_small_contours(self):
        # Remove all the small contours of less then 2000 mm^2
        # First decide which contours to remove.
        # Then remove the contours from the list with contours and areas
        for i, area in enumerate(self.area_list):
            if area < 2000:
                self.index_to_remove.append(i)
            
        for index in sorted(self.index_to_remove, reverse=True):
            del self.contour[index]
            del self.area_list[index]
       
    def display(self):
        # Display all the contours on the original picture.
        for (i, c) in enumerate(self.contour):
            ((x, y), _) = cv2.minEnclosingCircle(c)
            cv2.putText(self.image, "#{}".format(i + 1), (int(x) - 45, int(y)+20),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
            cv2.drawContours(self.image, [c], -1, (0, 255, 0), 2)

    def get_amout_of_contours(self):
        # Return the amout of contours.
        return(len(self.area_list))

    def get_areas_of_contours(self):
        # Return the list with the found areas and the total area of all the contours.
        for index in range(len(self.area_list)):
            self.total_area = self.total_area + self.area_list[index]
        return(self.area_list, self.total_area)

    def show_image(self):
        # Function for displaying the images.
        self.display()
        cv2.imshow('opening', self.opening)
        cv2.imshow('final', self.image)
        cv2.waitKey()
        cv2.destroyAllWindows()
        
if __name__ == '__main__':
    contours = contours('scans/objects_0.jpg')
    contours.filters()
    contours.contours()
    print(contours.get_areas_of_contours())
    contours.show_image() 
