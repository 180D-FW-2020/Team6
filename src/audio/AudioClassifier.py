"""
@author: Robert Renzo Rudio
@date: Tue Nov 17 19:37:25 2020
"""

# Libraries
from tensorflow import keras

class AudioClassifier:
    def __init__(self, model_path):
        self.model = keras.models.load_model(model_path)
        self.in_dim = self.model.input_shape[1]
        self.le_mappings = {0: "baby", 1: "enviroment"}
        
    def fit(self, X, y):
        pass

    def model_summary(self):
        self.model.summary()
    
    def predict(self, X):
        labels = (self.model.predict(X) > 0.5).astype("int32")
        labels = [self.le_mappings[i[0]] for i in labels]
        return labels[0]