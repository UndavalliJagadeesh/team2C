import cv2
import numpy as np
import os
import tensorflow as tf

np.random.seed(20)


class Detector:
    def __init__(self):
        self.detectedObjects = []

    def readClasses(self, classesFilePath):
        with open(classesFilePath, 'r') as f:
            self.classesList = f.read().splitlines()
        self.colorList = np.random.uniform(low=0, high=225, size=(len(self.classesList), 3))


    def loadModel(self):
        tf.keras.backend.clear_session()
        self.model = tf.saved_model.load(os.path.join("./saved_model"))

    def createBoundingBox(self, image, threshold=0.5):
        inputTensor = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2RGB)
        inputTensor = tf.convert_to_tensor(inputTensor, dtype=tf.uint8)
        inputTensor = inputTensor[tf.newaxis, ...]

        detections = self.model(inputTensor)

        bboxs = detections['detection_boxes'][0].numpy()
        classIndexes = detections['detection_classes'][0].numpy().astype(np.int32)
        classScores = detections['detection_scores'][0].numpy()

        imH, imW, imC = image.shape

        bboxIdx = tf.image.non_max_suppression(bboxs, classScores, max_output_size=4,
                                               iou_threshold=threshold, score_threshold=threshold)

        if len(bboxIdx) != 0:
            for i in bboxIdx:
                bbox = tuple(bboxs[i].tolist())
                class_confidence = round(100 * classScores[i])
                class_index = classIndexes[i]
                class_label_text = self.classesList[class_index].upper()
                class_color = self.colorList[class_index]
                display_text = '{}: {}%'.format(class_label_text, class_confidence)

                self.detectedObjects.append(class_label_text)

                ymin, xmin, ymax, xmax = bbox
                xmin, xmax, ymin, ymax = (xmin * imW, xmax * imW, ymin * imH, ymax * imH)
                xmin, xmax, ymin, ymax = int(xmin), int(xmax), int(ymin), int(ymax)

                cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color=class_color, thickness=1)
                # cv2.putText(image, display_text, (xmin, ymin - 10), cv2.FONT_HERSHEY_PLAIN, 1, class_color, 2)

                line_width = min(int((xmax - xmin) * 0.2), int((ymax - ymin) * 0.2))

                cv2.line(image, (xmin, ymin), (xmin + line_width, ymin), class_color, thickness=5)
                cv2.line(image, (xmin, ymin), (xmin, ymin + line_width), class_color, thickness=5)
                cv2.line(image, (xmax, ymin), (xmax - line_width, ymin), class_color, thickness=5)
                cv2.line(image, (xmax, ymin), (xmax, ymin + line_width), class_color, thickness=5)

                cv2.line(image, (xmin, ymax), (xmin + line_width, ymax), class_color, thickness=5)
                cv2.line(image, (xmin, ymax), (xmin, ymax - line_width), class_color, thickness=5)
                cv2.line(image, (xmax, ymax), (xmax - line_width, ymax), class_color, thickness=5)
                cv2.line(image, (xmax, ymax), (xmax, ymax - line_width), class_color, thickness=5)

        return image

    def predictImage(self, imagePath, threshold):
        image = cv2.imread(imagePath)
        bboxImage = self.createBoundingBox(image, threshold)
        return bboxImage
