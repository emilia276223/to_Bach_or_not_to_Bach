from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsOneClassifier

class LogReg(BaseModel):
    '''
        ovo - False for 1 vs rest, True for 1 vs 1
    '''
    def fit(self, ovo=False):
        model = LogisticRegression(max_iter=50000, class_weight='balanced')
        if ovo:
            model = OneVsOneClassifier(model)
        self.model = model
        self.model.fit(self.X_train, self.Y_train)
