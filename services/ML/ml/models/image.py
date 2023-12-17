import os
from functools import lru_cache

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
    image = image.transpose(2, 0, 1)
    image = image[np.newaxis, :]
    return image


model_paths = [
    "ml/models/weights/model.onnx",
    "./weights/model.onnx",
]


class MatchingModel:
    def __init__(self):
        # ai-goods-backend/services/ML/ml/models/weights/model.onnx

        while len(model_paths) > 0:
            path = model_paths.pop(0)
            try:
                self.sess = onnxruntime.InferenceSession(path)
                break
            except Exception:
                continue
        else:
            raise Exception("Can't load model")

        self.input_name = self.sess.get_inputs()[0].name

    def run(self, image: np.ndarray) -> list[float]:
        model_output = self.sess.run(None, {self.input_name: image})

        # model_output: [ndarray[1, 512]]
        embedding = model_output[0][0].tolist()
        return embedding


@lru_cache()
def get_matching_model():
    return MatchingModel()  # add caching class to avoid loading model each time
