import cv2
import numpy as np

class yolo():
    def __init__(self, name_image):
        self.image = cv2.imread(name_image)

        self.Width = self.image.shape[1]
        self.Height = self.image.shape[0]
        self.scale = 0.00392 # if one it can see in the small box a table.

        with open('yolov3/yolov3.txt', 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]

        self.COLORS = np.random.uniform(0, 255, size=(len(self.classes), 3))
        self.class_ids = []
        self.confidences = []
        self.boxes = []
        self.conf_threshold = 0.5
        self.nms_threshold = 0.4

        self.index_list = []
        self.object_list = []

    def detect_object(self):
        outs = self.blob_from_network()
        self.find_high_confidence_boxes(outs)
        self.non_max_supression()

    def blob_from_network(self):
        # Read deep learning network. (Trained weights, Text file containing network configuration)
        net = cv2.dnn.readNet('yolov3/yolov3.weights', 'yolov3/yolov3.cfg')

        # Creates 4-dimensional(NCHW) blob from image (number of images, channels of image rgb=3 gray = 1, height, width). 
        # (input image, scaling, size, the mean of the colors, swap red and blue, crop image)
        blob = cv2.dnn.blobFromImage(self.image, self.scale, (416,416), (0,0,0), True, crop=False)

        # Set the blob as input for the deep learing network
        net.setInput(blob)

        # 4-dimensional(NCHW) blob for first output of specified layer
        outs = net.forward(self.get_output_layers(net))
        return outs

    def find_high_confidence_boxes(self, outs):
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * self.Width)
                    center_y = int(detection[1] * self.Height)
                    w = int(detection[2] * self.Width)
                    h = int(detection[3] * self.Height)
                    x = center_x - w / 2
                    y = center_y - h / 2
                    self.class_ids.append(class_id)
                    self.confidences.append(float(confidence))
                    self.boxes.append([x, y, w, h])

    def non_max_supression(self):
        indices = cv2.dnn.NMSBoxes(self.boxes, self.confidences, self.conf_threshold, self.nms_threshold)

        for i in indices:
            i = i[0]
            box = self.boxes[i]
            x = box[0]
            y = box[1]
            w = box[2]
            h = box[3]
            self.create_index_list_of_object(self.class_ids[i])
            self.create_name_of_object(self.class_ids[i])
            self.draw_prediction(self.image, self.class_ids[i], self.confidences[i], round(x), round(y), round(x+w), round(y+h))

    def get_output_layers(self, net):
        # returns layer names
        layer_names = net.getLayerNames()

        # remove unconnected outputs from the layer name list.
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        return output_layers

    def draw_prediction(self, img, class_id, confidence, x, y, x_plus_w, y_plus_h):
        label = str(self.classes[class_id]) + ', ' + str(round(confidence,1))
        color = self.COLORS[class_id]
        cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)
        cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    def create_index_list_of_object(self, i):
        self.index_list.append(i)

    def create_name_of_object(self, class_id):
        self.object_list.append(str(self.classes[class_id]))

    def get_index_list(self):
        return self.index_list

    def get_name_of_object(self):
        return len(self.object_list), self.object_list

    def show_image(self):
        cv2.imshow("object detection", self.image)
        cv2.waitKey()
        cv2.destroyAllWindows()
        
if __name__ == '__main__':
    detect = yolo('scans/objects_0.jpg')
    detect.detect_object()
    print(detect.get_name_of_object())
    detect.show_image()