from sklearn.neighbors import KNeighborsClassifier

class KNN(BaseModel):
    '''
    Takes:
        optionally n_neighbors - at how many neighbors should KNN look (default = 3)
        optionally weights - "uniform" is default, the other option is "distance"
    Calculates: X_train, X_test, Y_train, Y_test, model
    '''
    def fit(self, n_neighbors=7, weights="distance"):
        self.model = KNeighborsClassifier(n_neighbors=n_neighbors, weights=weights)
        self.model.fit(self.X_train, self.Y_train)
