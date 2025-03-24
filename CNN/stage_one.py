# Authors: Vithusha (Metha) Tharmarasa, MinYoung Park
# Last Modified: Mar. 23rd, 2024

# Stage 1: Determines whether there is a fracture

import tensorflow as tf
from typing import Tuple


class BinaryFractureClassifier:
    def __init__(self, input_shape: Tuple[int, int, int]):
        self.model = self.build_model(input_shape)
        self.compile_model()

    def build_model(self, input_shape: Tuple[int, int, int]) -> tf.keras.Model:
        model = tf.keras.models.Sequential([
            tf.keras.layers.Input(shape = input_shape, dtype = tf.float64),
            tf.keras.layers.Conv2D(32, (3, 3), activation = "relu", padding = "same"),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Conv2D(64, (3, 3), activation = "relu", padding = "same"),
            tf.keras.layers.MaxPooling2D((2, 2,)),
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.Dense(64, activation = "relu"),
            tf.keras.layers.Dense(1, activation = "sigmoid")
        ])

        return model

    def compile_model(self):
        self.model.compile(
            optimizer = tf.keras.optimizers.Adam(),
            loss = tf.keras.losses.BinaryCrossentropy(),
            metrics = ["accuracy"]
        )