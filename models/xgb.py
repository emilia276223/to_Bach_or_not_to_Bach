from xgboost import XGBClassifier

from models.base_model import BaseModel

class XGB(BaseModel):
    def fit(self):
        self.model = XGBClassifier(objective='multi:softmax', num_class=10, n_estimators=150, colsample_bytree=0.8)
        self.model.fit(self.X_train, self.Y_train)
