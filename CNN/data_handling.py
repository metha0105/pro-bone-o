# Authors: Vithusha (Metha) Tharmarasa, MinYoung Park
# Last Modified: Mar. 22nd, 2024

import os
import re
import tensorflow as tf
import numpy as np
import skrf as rf # for reading .s2p files
import random
import matplotlib.pyplot as plt

from typing import List, Tuple
from collections import defaultdict
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
        filename_array = []
        data_array = []
        class_array = []

        for subdir, _, files in os.walk(self.data_dir):
            for file in files:
                if re.search("(.s2p)", file):
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
        split_correctly = False

        while split_correctly == False:
            indices = random.sample(range(len(data_array)), len(data_array))
            shuffled_data_samples = [data_array[i] for i in indices]
            shuffled_class_labels = [class_array[i] for i in indices]

            train_samples = shuffled_data_samples[:(len(shuffled_data_samples) // 10) * 8]
            train_labels = shuffled_class_labels[:(len(shuffled_class_labels) // 10) * 8]
            test_samples = shuffled_data_samples[(len(shuffled_data_samples) // 10) * 8:]
            test_labels = shuffled_class_labels[(len(shuffled_class_labels) // 10) * 8:]

            if set(train_labels) == set(test_labels):
            # Only exit if both train and test has the same number of classes
                split_correctly = True
            else:
                split_correctly = False
        return train_samples, train_labels, test_samples, test_labels
    
    def data_to_tensor(train_samples, train_labels, test_samples, test_labels):
        # Load NumPy array with tensorflow docs
        # https://www.tensorflow.org/tutorials/load_data/numpy#load_numpy_arrays_with_tfdatadataset
        train_samples = tf.ragged.constant(train_samples, dtype=tf.complex128).to_tensor()
        train_real_samples = tf.math.real(train_samples)
        train_imag_samples = tf.math.imag(train_samples)
        #tf.print(train_real_samples, train_imag_samples, output_stream=os.sys.stderr, sep='\n\nXXXXXXXXX\n\n', summarize=None)
        train_complex_samples = tf.concat([train_real_samples, train_imag_samples], -1)
        #tf.print(train_complex_samples, output_stream=os.sys.stderr, summarize=None)
        train_labels = tf.convert_to_tensor(train_labels, dtype=tf.float64)


        # Currently debugging the test dataset because I think the label bit is broken from the split
        test_samples = tf.ragged.constant(test_samples, dtype=tf.complex128).to_tensor()
        test_real_samples = tf.math.real(test_samples)
        test_imag_samples = tf.math.imag(test_samples)
        test_complex_samples = tf.concat([test_real_samples, test_imag_samples], -1)
        test_labels = tf.convert_to_tensor(test_labels, dtype=tf.float64)

        # Debugging line to determine if these tensors are outputting correctly
        #tf.print(train_complex_samples, train_labels, output_stream=os.sys.stderr, sep='\n\nXXX\n\n', summarize=None)
        #tf.print(test_complex_samples, test_labels, output_stream=os.sys.stderr, sep='\n\nXXX\n\n', summarize=-1)

        print(train_complex_samples.shape)
        return train_complex_samples, train_labels, test_complex_samples, test_labels