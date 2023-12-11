import os

import cv2
import numpy as np
import onnxruntime


def normalize_image(image):
    mean = [0.485, 0.456, 0.406]
    std = [0.229, 0.224, 0.225]
    image = image.astype(np.float32)

    image /= 255.0
    for i in range(image.shape[2]):
        image[:, :, i] = (image[:, :, i] - mean[i]) / std[i]
    
    image = cv2.resize(image, (224, 224))
    image = image.transpose(2,0,1)
    image = image[np.newaxis, :]
    return image

class MatchingModel():
    def __init__(self):
        self.sess = onnxruntime.InferenceSession("/Users/dmitrykutsenko/Desktop/ai-goods-backend/services/ML/ml/models/weights/model.onnx")
        self.input_name = self.sess.get_inputs()[0].name

    def run(self, array):
        result = self.sess.run(None, {self.input_name: array})[0]
        return result
