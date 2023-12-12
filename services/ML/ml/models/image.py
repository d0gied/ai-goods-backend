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


class MatchingModel:
    def __init__(self):
        # ai-goods-backend/services/ML/ml/models/weights/model.onnx
        weights_path = "./weights/model.onnx"

        self.sess = onnxruntime.InferenceSession(weights_path)
        self.input_name = self.sess.get_inputs()[0].name

    def run(self, images: np.ndarray | list[np.ndarray]) -> np.ndarray:
        if isinstance(images, list):
            images = np.array(images)

        model_output: list[tuple[np.ndarray, dict]] = self.sess.run(
            None, {self.input_name: images}
        )  # list: (embeddings: np.ndarray, dict: {???})

        embeddings = []
        for output in model_output:
            embeddings.append(output[0].tolist())  # get embeddings from output

        return embeddings


@lru_cache()
def get_matching_model():
    return MatchingModel()  # add caching class to avoid loading model each time
