"""
@author: Robert Renzo Rudio
@date: Tue Nov 17 19:37:25 2020
"""

# Libraries
import numpy as np
import os
import sys
import threading
from tensorflow import keras
from pathlib import Path

SRCPATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTIFPATH = os.path.join(SRCPATH, 'notification')
sys.path.append(NOTIFPATH)
import notification #pylint: disable=import-error

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
        self.le_mappings = {0: 'animals', 1: 'baby', 2: 'exterior', 3: 'interior', 4: 'nature'}
        
    def fit(self, X, y):
        pass

    def model_summary(self):
        """Neural network to be used for classification
        """
        self.model.summary()
    
    
    def predict(self, X):
        thread = threading.Thread(target=self._predict, args=(X,))
        thread.start()

    def _predict(self, X):
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
        print("├── Classifying Noise ...", end="\r")
        X = np.array([np.float32(X)])
        X = X.reshape(X.shape[0], self.r, self.c, self.ch) # pylint: disable=unsubscriptable-object, too-many-function-args 

        label = self.model.predict(X)
        clas = np.argmax(label, axis=-1)
        clas = self.le_mappings[clas[0]]
        prob = np.amax(label / np.sum(label) * 100, axis=-1)[0]
        print("├── Classifying Noise ... Done")
        
        print("├── Pushing Notification ...", end="\r")
        msg = f"Noise came from {clas} with %{prob:.2f} probability"
        self.push_notification(msg)
        print("├── Pushing Notification ... Done")

        print("├── Recording for Storage ...", end="\r")
    
    def push_notification(self, msg):
        subject = "Noise Detected"
        notification.notify(subject, msg)