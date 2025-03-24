# Authors: Vithusha (Metha) Tharmarasa, MinYoung Park
# Last Modified: Mar. 24th, 2025

# Runs stage 1 (i.e., binary classification to check whether there is a fracture)
from data_handling import DataProcessing
from stage_one import BinaryFractureClassifier

data_dir = "TBD"
dataset = DataProcessing(data_dir, multi_class = False)
data_samples, data_labels = dataset.load_data()
train_samples, train_labels, test_samples, test_labels = dataset.split_data(data_samples, data_labels)
train_data, train_labels = dataset.data_to_tensor(train_samples, train_labels)
test_data, test_labels = dataset.data_to_tensor(test_samples, test_labels)

classifier = BinaryFractureClassifier(input_shape = (train_data.shape[1], train_data.shape[2], train_data.shape[3]))
classifier.model.fit(train_data, train_labels, epochs = 15, batch_size = 64, validation_data = (test_data, test_labels))
classifier.model.evaluate(test_data, test_labels)