# Importing all the modules required.

import numpy as np

from sklearn.model_selection import train_test_split, GridSearchCV

from sklearn.preprocessing import Normalizer

from sklearn.metrics import classification_report, confusion_matrix

from sklearn.pipeline import make_pipeline

from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

from sklearn.svm import SVC

from json import dumps

import pickle

import os

import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

class classification():

    # Class to handle classification model

    def __init__(self,model_list = ['SVC','KNN', 'RF', 'LR', 'DTC'] ) -> None:

        self.x_normalizer = None
        
        self.model_to_be_used = {
            'SVC': False,
            'KNN': False,
            'RF': False,
            'LR': False,
            'DTC': False
        }

        self.model_dict = {
            'SVC': SVC,
            'KNN': KNeighborsClassifier,
            'RF': RandomForestClassifier,
            'LR': LogisticRegression,
            'DTC': DecisionTreeClassifier,
        }

        self.model_trained = {
            'SVC': None,
            'KNN': None,
            'RF': None,
            'LR': None,
            'DTC': None,
        }

        self.model_trained_details = {
            'SVC': 0,
            'KNN': 0,
            'RF': 0,
            'LR': 0,
            'DTC': 0,
        }

        

        self.hyperparameters = {
            'SVC': {
                'C': [0.001, 0.01, 0.1, 1],
                'kernel': ['linear', 'poly', 'rbf'],
                'gamma': ['scale', 'auto']
            },

            'KNN': {
                'n_neighbors': [1, 3, 5, 10, 20],
                'weights': ['uniform', 'distance'],
            },

            'RF': {
                'max_depth': [20, 50, 100, None],  
                'criterion': ['gini', 'entropy'],
                'n_estimators': [200, 250, 300],
            },

            'LR': {
                'C': [0.001, 0.01, 0.1, 1]
            },

            'DTC': {
                'criterion': ['gini', 'entropy'],
                'max_depth': [10, 20, 50, 70, 100, 150, None]   
            }
        }

        for model_name in model_list:
            if model_name.upper() in self.model_to_be_used:
                self.model_to_be_used[model_name.upper()] = True

        
    def fit(self, x_train, y_train, cvReport: bool = True ) -> None:

        self.x_train = x_train
        self.y_train = y_train

        self.x_normalizer = Normalizer().fit(x_train)
        x_train_normalized = self.x_normalizer.transform(x_train)

        for model_name in self.model_to_be_used:
            if self.model_to_be_used[model_name]:

                model = GridSearchCV(
                    self.model_dict[model_name](),
                    self.hyperparameters[model_name],
                    cv=5
                ) 

                model.fit(x_train_normalized, self.y_train)

                self.model_trained[model_name] = model

                mean_fit_time= model.cv_results_['mean_fit_time']
                mean_score_time= model.cv_results_['mean_score_time']


                self.model_trained_details[model_name] = {
                   "acc": model.best_score_,
                   "mean_fit_time": np.mean(mean_fit_time) ,
                   "mean_score_time": np.mean(mean_score_time),
                }

                if cvReport:
                    self._GridSearch_Report(model_name, model)
            
        print()
        print()
        print("Final Accuracy")
        print(dumps(self.model_trained_details, indent=2))

                
    
    def _GridSearch_Report(self, model_name:str, clf: GridSearchCV):
        print()
        print(f'Model: {model_name}')
        print()
        print(f'Prameters : {clf.best_params_}')
        print(f'Score : {clf.best_score_}')
        print()

        means = clf.cv_results_['mean_test_score']
        stds = clf.cv_results_['std_test_score']
        for mean, std, params in zip(means, stds, clf.cv_results_['params']):
            print(f"{mean:.3f} (+/-{std*2:0.03f}) for {params}")

        print()
        print('#'*20)
    

    def classification_report(self, model_name: str, x_test, y_test )-> None:

        if self._check_model_exit_trained(model_name):


            y_predict = self.predict(model_name, x_test)

            print()
            print('#'*20)
            print(f'Model name : {model_name}')
            print('#'*20)
            print()
            print(classification_report(y_test, y_predict))
            print()

       



    def predict(self, model_name:str, x_test ) -> None:

        if self._check_model_exit_trained(model_name):

            x_test_normalized = self.x_normalizer.transform(x_test)
            return self.model_trained[model_name].predict(x_test_normalized)
    
    

    def save_model(
        self,
        model_name:str, 
        parameters: dict = None,
        model_file_name:str = None, 
        model_path:str = None) -> None:
        
        if self._check_model_exit_trained(model_name):

            if parameters is None:
                parameters = self.model_trained[model_name].best_params_

            if model_file_name is None:
                model_file_name = f'{model_name}.pkl'
            
            if model_path is None :
                model_path = './'
            
            if not os.path.isdir(model_path):
                raise Exception(f"{model_path} does not exist")
            
            final_path = os.path.join(model_path, model_file_name)

        
            
            pipeline = make_pipeline(
                Normalizer(), 
                self.model_dict[model_name](**parameters)
                )
            
            pipeline.fit(self.x_train, self.y_train)
            
            with open(final_path, 'wb') as model_file:
                pickle.dump(pipeline, model_file)

                
                

    def _check_model_exit_trained(self, model_name: str) ->bool:

        model_name = model_name.upper()
        
        if model_name in self.model_trained:

            if self.model_trained[model_name] is not None and self.x_normalizer is not None:
                return True

            else:
                raise Exception(f'"{model_name}" is not trained')
        else:
            raise Exception(f'There is no "{model_name}" model.')