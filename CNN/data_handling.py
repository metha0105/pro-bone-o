# Authors: Vithusha (Metha) Tharmarasa, MinYoung Park
# Last Modified: Mar. 24th, 2024

import os
# import re
import tensorflow as tf
# import numpy as np
import skrf as rf
from sklearn.model_selection import train_test_split

class DataProcessing:
    def __init__(self, data_dir: str, train_ratio: float = 0.8, multi_class: bool = False):
        self.data_dir = data_dir
        self.train_ratio = train_ratio
        self.multi_class = multi_class

        if not multi_class:
            self.class_mapping = {
                "empty": 0,
                "non-fractured": 0,
                "greenstick": 1,
                "hairline": 1,
                "comminuted": 1,
                "oblique": 1,
                "transverse": 1
            }
        else:
            self.class_mapping = {
                "greenstick": 0,
                "hairline": 1, 
                "comminuted": 2, 
                "oblique": 3,
                "transverse": 4
            }
    
    def load_data(self):
        filename_array, data_array, class_array = [], [], []

        for subdir, _, files in os.walk(self.data_dir):
            for file in files:
                if file.endswith(".s2p"):
                    curr_filename = os.path.join(subdir, file)
                    curr_data = rf.Network(curr_filename).s
                    curr_class_label = self.class_mapping.get(subdir.replace(self.data_dir + "\\", "").strip(), 0)

                    filename_array.append(curr_filename)
                    data_array.append(curr_data)
                    class_array.append(curr_class_label)
                else:
                    print(f"Skipping invalid file: {file}")
        
        return data_array, class_array
    
    def split_data(self, data_array, class_array):
        train_samples, test_samples, train_labels, test_labels = train_test_split(
            data_array, class_array, test_size = 1 - self.train_ratio, stratify = class_array, random_state = 42
        )
        return train_samples, train_labels, test_samples, test_labels
    
    def data_to_tensor(self, train_samples, train_labels, test_samples, test_labels):
        train_samples = tf.ragged.constant(train_samples, dtype=tf.complex128).to_tensor()
        train_real_samples = tf.math.real(train_samples)
        train_imag_samples = tf.math.imag(train_samples)
        train_complex_samples = tf.concat([train_real_samples, train_imag_samples], -1)
        train_labels = tf.convert_to_tensor(train_labels, dtype=tf.float64)

        test_samples = tf.ragged.constant(test_samples, dtype=tf.complex128).to_tensor()
        test_real_samples = tf.math.real(test_samples)
        test_imag_samples = tf.math.imag(test_samples)
        test_complex_samples = tf.concat([test_real_samples, test_imag_samples], -1)
        test_labels = tf.convert_to_tensor(test_labels, dtype=tf.float64)

        print(f"Train Samples Shape: {train_complex_samples.shape}")
        print(f"Test Samples Shape: {test_complex_samples.shape}")

        return train_complex_samples, train_labels, test_complex_samples, test_labels

    def print_data_stats(self, train_labels, test_labels):
        print("Training Set Class Distribution:", {i: train_labels.count(i) for i in set(train_labels)})
        print("Test Set Class Distribution:", {i: test_labels.count(i) for i in set(test_labels)})