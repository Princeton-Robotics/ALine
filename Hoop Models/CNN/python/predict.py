import sys
import cv2 as cv
import imutils as utils
import tensorflow as tf
import numpy as np
from PIL import Image
from object_detection import ObjectDetection

MODEL_FILENAME = 'model.pb'
LABELS_FILENAME = 'labels.txt'

class TFObjectDetection(ObjectDetection):
    """Object Detection class for TensorFlow
    """
    def __init__(self, graph_def, labels):
        super(TFObjectDetection, self).__init__(labels)
        self.graph = tf.Graph()
        with self.graph.as_default():
            tf.import_graph_def(graph_def, name='')
            
    def predict(self, preprocessed_image):
        inputs = np.array(preprocessed_image, dtype=np.float)[:,:,(2,1,0)] # RGB -> BGR

        with tf.Session(graph=self.graph) as sess:
            output_tensor = sess.graph.get_tensor_by_name('model_outputs:0')
            outputs = sess.run(output_tensor, {'Placeholder:0': inputs[np.newaxis,...]})
            return outputs[0]


def main(image_filename):
    # Load a TensorFlow model
    graph_def = tf.GraphDef()
    with tf.gfile.FastGFile(MODEL_FILENAME, 'rb') as f:
        graph_def.ParseFromString(f.read())

    # Load labels
    with open(LABELS_FILENAME, 'r') as f:
        labels = [l.strip() for l in f.readlines()]

    od_model = TFObjectDetection(graph_def, labels)

    image = Image.open(image_filename)
    cvImage = cv.imread(image_filename)
    predictions = od_model.predict_image(image)
    print(predictions)

    width, height = image.size
    print("IMAGE: ", width, height)

    prediction = predictions[0]
    leftXCoor = int(prediction['boundingBox']['left'] * width)
    leftYCoor = int(prediction['boundingBox']['top'] * height)
    sizeX = prediction['boundingBox']['width'] * width
    sizeY = prediction['boundingBox']['height'] * height
    rightXCoor = int(leftXCoor + sizeX)
    rightYCoor = int(leftYCoor + sizeY)
    print(leftXCoor, leftYCoor)

    kernel = np.array((
        [-1,-1,-1],
        [-1,8,-1],
        [-1,-1,-1]
    ))

    # cvImage = cvImage[leftXCoor:rightXCoor,leftYCoor:rightYCoor]
    # lines = cv.filter2D(cvImage[:,:,2], -1, kernel)
    leftXCoor = max(0, leftXCoor)
    leftYCoor = max(0, leftYCoor)
    rightXCoor = min(rightXCoor, width - 1)
    rightYCoor = min(rightYCoor, height - 1)

    # lines = cv.filter2D(cvImage[leftXCoor:rightXCoor,leftYCoor:rightYCoor,:2], -1, kernel)

    # th, dst = cv.threshold(lines, 100, 255, cv.THRESH_BINARY)

    # lines = cv.HoughLines(dst, 1, np.pi/180 , 70)

    if (0):
        for line in lines:
            for rho, theta in line:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho
                y0 = b*rho
                x1 = int(x0 + 1000*(-b))
                y1 = int(y0 + 1000*(a))
                x2 = int(x0 - 1000*(-b))
                y2 = int(y0 - 1000*(a))

                # cv.line(cvImage,(x1,y1),(x2,y2),(0,255,0),2)
    
    cv.rectangle(cvImage, (leftXCoor, leftYCoor), (rightXCoor, rightYCoor), (255, 0, 0), 2)

    cv.imshow("img", utils.resize(cvImage, width = 600))
    cv.waitKey(0)
    cv.destroyAllWindows()


    
if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('USAGE: {} image_filename'.format(sys.argv[0]))
    else:
        main(sys.argv[1])
