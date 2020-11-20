"""
@author: Robert Renzo Rudio
@date: Tue Nov 17 19:37:25 2020
"""

# Libraries
from tensorflow import keras
import numpy as np

class AudioClassifier:
    """
    A class used to classify audio into "baby" or "environment"
    
    Attributes
    ----------
    self.model : keras.model
        Neural network to be used for classification
    self.in_dim : tuple
        Neural netowrk's input dimension
    self.le_mappings : dict
        mappings from int to string label

    Methods
    -------
    mode_summary(self)
        Prints neural network's topology.
    predict(self, X)
        Predict X's label using the neural network.
    """

    def __init__(self, model_path):
        """
        Parameters
        ----------
        self.model : keras.model
            Neural network to be used for classification
        self.in_dim : tuple
            Neural netowrk's input dimension
        self.le_mappings : dict
            mappings from int to string label
        """
        self.model = keras.models.load_model(model_path)
        self.in_dim = self.model.input_shape
        self.r, self.c, self.ch = self.in_dim[1:]
        self.le_mappings = {0: "baby", 1: "enviroment"}
        
    def fit(self, X, y):
        pass

    def model_summary(self):
        """Neural network to be used for classification
        """
        self.model.summary()
    
    def predict(self, X):
        """Predict X's label using the neural network

        Parameters
        ----------
        X : np
            Audio to be classified

        Returns
        -------
        labels : str
            The predicted label of X
        """
        print("Predicting ...")
        X = np.array([np.float32(X)])
        X = X.reshape(X.shape[0], self.r, self.c, self.ch) # pylint: disable=unsubscriptable-object, too-many-function-args 
        #label = (self.model.predict(X) > 0.5).astype("int32")
        label = np.argmax(self.model.predict(X), axis=-1)
        print(label)
        return "baby"
        return label[0][0]