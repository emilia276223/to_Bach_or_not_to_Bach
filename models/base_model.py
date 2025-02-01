import json

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report

class BaseModel:
    def __init__(self, dataset):
        self.X_train = dataset.X_train
        self.X_test = dataset.X_test
        self.Y_train = dataset.Y_train
        self.Y_test = dataset.Y_test
        self.features_names = dataset.features_names
        self.composers_names = dataset.composers_names

        self.model = None
        self.Y_pred = None
        self.report = None
        self.conf_matrix = None

    def predict(self):
        self.Y_pred = self.model.predict(self.X_test)

    def print_metrics(self):
        print(f"{self.__class__.__name__} - Final Classification Report:")
        self.report = classification_report(self.Y_test, self.Y_pred, target_names=self.composers_names)
        print(self.report)

        self.conf_matrix = confusion_matrix(self.Y_test, self.Y_pred)

        plt.figure(figsize=(8, 6))
        sns.heatmap(self.conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=self.composers_names, yticklabels=self.composers_names)
        plt.xlabel('Predicted Labels')
        plt.ylabel('True Labels')
        plt.title(f'{self.__class__.__name__} - Confusion Matrix')
        plt.show()

    def save_metrics(self, filename):
        with open(filename, "w") as f:
            f.write(json.dumps(self.conf_matrix.tolist()))
