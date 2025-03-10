from sklearn.svm import SVC

from models.base_model import BaseModel

class SVM(BaseModel):
    def fit(self):
        self.model = SVC(kernel='rbf', decision_function_shape='ovo')
        self.model.fit(self.X_train, self.Y_train)
