import json
import os

import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler



'''
How to use:
    dataset = DataSet(data_dir)
    dataset.process_data() ---> creates X_data, Y_data: whole dataset, no splitting yet
    dataset.split_data() -----> splits into X_train, X_test, Y_train, Y_test
    dataset.print_class_distribution ---> as name says, just for presentation purposes
And then you can directly access members:
    dataset.X_data
    dataset.Y_data
    dataset.X_train
    dataset.X_test
    dataset.Y_train
    dataset.Y_test
    dataset.features_names
    dataset.composers_names
'''

class DataSet:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.features_done = False
        self.features_names = np.array([])    # 1D arary of size (n_features)
        self.composers_names = [
            "Bach", "Beethoven", "Brahms", "Chopin", "Haendel", "Haydn", "Mozart", "Schubert", "Schumann", "Vivaldi",
        ]   # 1D array of size (n_composers)

        self.X_data = np.empty((0,407))       # 2D array of size (n_samples, n_features)
        self.Y_data = np.array([])            # 1D array of size (n_samples,)
        self.X_train = None
        self.X_test = None
        self.Y_train = None
        self.Y_test = None

    '''
    Takes: file .json
    Returns: 1D array with int elements made from features' values
    How: iterates over json items and creates it "manually"
    '''
    def flatten_json(self, file):
        with open(file, 'r') as raw_json:
            dict_input = json.load(raw_json)

            np_input = np.array([])
            for key, value in dict_input.items():
                current_name = key

                if key == "key_signature":    # change true/false to numeric
                    if value[1]:
                        value[1] = 1
                    else:
                        value[1] = 0

                if isinstance(value, dict):   # nested dict
                for inkey, invalue in value.items():
                    tmp_current_name = current_name + "." + inkey
                    np_input = np.append(np_input, invalue)
                    if not self.features_done:
                    self.features_names = np.append(self.features_names, tmp_current_name)
                else:   # single element or list
                    np_input = np.append(np_input, value)
                    if not self.features_done:
                        self.features_names = np.append(self.features_names, current_name)

            self.features_done = True
            return np_input

    '''
    Takes: nothing
    Calculates: X_data - 2D array of size (n_samples, n_features), Y_data - 1D array of size (n_samples,), features_names - 1D arary of size (n_features)s, composers_names - 1D array of size (n_composers)
    How: iterates over subdirectories and files in them
    '''
    def process_data(self):
        for subdir, dirs, files in os.walk(self.data_dir):
            subdir_name = subdir.split("/")[-1]
            print(f"Working in subdirectory {subdir_name}")
            composer_name = subdir_name.title()

            for file in files:
                np_input = self.flatten_json(os.path.join(subdir, file))
                np_input = np_input.reshape(1, -1)
                self.X_data = np.append(self.X_data, np_input, axis = 0)
                self.Y_data = np.append(self.Y_data, self.composers_names.index(composer_name))

    '''
    Takes: nothing
    Calculates: X_train, X_test, Y_train, Y_test with scaler and balanced splitting
    '''
    def split_data(self):
        # Normalize the feature data
        scaler = StandardScaler()
        X_data_scaled = scaler.fit_transform(self.X_data)

        # Split data into training and testing sets
        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(
            X_data_scaled, self.Y_data, test_size=0.2, stratify=self.Y_data, random_state=42
        )

    '''
    Takes: nothing
    Calculates and prints: distribution in every class for whole dataset, training dataset and testing dataset
    '''
    def print_class_distribution(self):
        print("Class distribution in original data:", np.bincount(self.Y_data.astype(int)))
        print("Class distribution in training set:", np.bincount(self.Y_train.astype(int)))
        print("Class distribution in testing set:", np.bincount(self.Y_test.astype(int)))
