from sklearn.neighbors import KNeighborsClassifier

from models.base_model import BaseModel

class KNN(BaseModel):
    '''
    Takes:
        optionally n_neighbors - at how many neighbors should KNN look (default = 3)
        optionally weights - "uniform" is default, the other option is "distance"
    Calculates: model
    '''
    def fit(self, n_neighbors=7, weights="distance"):
        self.model = KNeighborsClassifier(n_neighbors=n_neighbors, weights=weights)
        self.model.fit(self.X_train, self.Y_train)
