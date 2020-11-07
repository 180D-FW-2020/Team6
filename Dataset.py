# -*- coding: utf-8 -*-
"""
@author: Robert Renzo Rudio
@date: Fri Nov  6 16:45:31 2020
"""

# Imports
import os
import pandas as pd 
from glob import glob

class Dataset:
    """
    A class used to create a dataframe
    
    Attributes
    ----------
    file_extension : str
        File extension of the data
    extract_method : method
        A method to be used for creating the dataset
    args : type(extract_method-argument)
        Arguments needed for extract_method

    Methods
    -------
    set_extract_method(extract_method, args)
        Sets the method for creating the dataset
    create_dataset(path)
        Given a path, search for all files of file_type and create the dataset
    _create_dataset(paths)
        Helper function for create_dataset
    save_dataset(path)
        Save the dataset as a pickle file into to path
    """

    def __init__(self, file_extension: str, extract_method=None, args=None):
        """
        Parameters
        ----------
        file_extension : str
            File extension of the data, format: "*.file_extension"
        extract_method : method
            A method to be use for creating the dataset
        args : type(method arg)
            Arguments needed for extract_method
        """

        self.file_extension = file_extension
        self.extract_method = extract_method
        self.args = args

    def set_extract_method(self, extract_method, args):
        """Sets the method for creating the dataset

        Parameters
        ----------
        extract_method : method
            A method to be use for creating the dataset
        args : type(method extract_method)
            Arguments needed for extract_method
        """

        self.extract_method = extract_method
        self.args = args

    def create_dataset(self, path: list) -> pd:
        """Given a path, search for all files of file_type and create the dataset
        
        Parameters
        ----------
        path : str
            Parent directory of the datas. Assumes directory path contains child
            directory a,b,c,... where a is the label of datas in a and so on

        Returns
        -------
        pd
            The constructed dataframe 
        
        Raises
        ------
        Exception
            If extract method has not been set
        """

        if self.extract_method is None:
            raise Exception("Dataset extraction method has not beed set")

        # store all relative path to datas.
        paths = [y for x in os.walk(path) for y in glob(os.path.join(x[0], self.file_extension))]
        return self._create_dataset(paths)

    def _create_dataset(self, paths: list) -> pd:
        """Helper function for create_dataset
        
        Parameters
        ----------
        paths : str
            List of relative path to datas.
        
        Returns
        -------
        pd
            The constructed dataframe 
        """

        dataset = []
        for path in paths:
            # Data label is the directory name.
            label = os.path.dirname(path).split("/")[-1]

            # Extract the data
            if self.args:
                features = self.extract_method(path, self.args)
            else:
                features = self.extract_method(path)

            dataset.append([label, features])
    
        # Convert dataset into a pandas dataframe.
        df = pd.DataFrame(dataset, columns=("label", "features"))

        return df
    
    def save_dataset(self, dataset: pd, path: str):
        """Save the dataset as a pickle file into to path
        
        Parameters
        ----------
        dataset : pd
            Dataframe to be saved.
        path : stf
            Path to where the dataframe will be saved.
        """

        dataset.to_pickle(path)