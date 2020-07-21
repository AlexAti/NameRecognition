from NameRecognition.CSChar import CSChar
from NameRecognition.Transformer import *
from NameRecognition.Pipeline import Pipeline
from NameRecognition.ExtraFields import ExtraFields

import numpy as np
import pandas as pd


class BaseEstimator:
    '''
    Estimador base para la implementación de estimadores sobre la comparación 
    de nombres.
    '''
    def __init__(self):
        raise NotImplementedError

    def predict(self, df):
        raise NotImplementedError

    def fit(self, series):
        raise NotImplementedError

class BSEstimator(BaseEstimator):
    '''
    Estimador básico sobre la comparación de string por medio del algoritmo de
    distancia de Levenshtein.
    '''
    def __init__(self):
        raise NotImplementedError

    def predict(self, df):
        raise NotImplementedError

    def fit(self, series):
        raise NotImplementedError

class TMEstimator(BaseEstimator):
    '''
    Estimador básado en Text Mining sobre la estracción simple de 
    características textuales sobre frecuencias de n-gram caracteres.

    Estructura del algoritmo:
    1) Estandarización de nombres
    2) Limpieza de palabras poco representativas.
    3) Calculo de frecuencias
    4) Distancia coseno
    '''
    def __init__(self, 
        threshold = None, 
        score_factor = None,
        df_screen = None, 
        key_screen = None, 
        value_screen = None, 
        key_party = None, 
        value_party = None
    ):
        self.df_screen = df_screen
        self.key_screen = key_screen
        self.value_screen = value_screen
        self.key_party = key_party
        self.value_party = value_party
        self.threshold = threshold
        self.score_factor = score_factor

        self.pipeline = Pipeline(transform_list = [
            SNTransformer(),
            SWCTransformer()
        ])
        self.nr = CSChar(
            threshold = threshold['value_threshold'] / 100.0, 
            verbose = False
        )

    def fit(self, series):
        series = self.pipeline.fit_transform(series)
        self.nr.fit(series)
        if self.df_screen != None:
            self.df_screen['transform'] = self.pipeline.transform(self.df_screen[self.value_screen])

    def predict(self, df):
        df['transform'] = self.pipeline.transform(df[self.value_party])
        adjacency_matrix = self.nr.screen(
            df1 = self.df_screen,
            df2 = df,
            key1 = self.key_screen,
            key2 = self.key_party,
            value1 = 'transform',
            value2 = 'transform'
        )
        return(adjacency_matrix)

    def set_df_screen(self, df_screen):
        self.df_screen = df_screen
        self.df_screen['transform'] = self.pipeline.transform(self.df_screen[self.value_screen])

class NNEstimator(BaseEstimator):
    '''
    Estimador optimizado por redes neuronales densas sobre el estimador 
    Text Mining.
    '''
    def __init__(self):
        raise NotImplementedError

    def predict(self, df):
        raise NotImplementedError

    def fit(self, parameter_list):
        raise NotImplementedError

class DLEstimator(BaseEstimator):
    '''
    Estimador optimizado por redes neuronales convolucionales sobre técnicas
    de Deep Learning y Embeddings.
    '''
    def __init__(self):
        raise NotImplementedError

    def predict(self, df):
        raise NotImplementedError

    def fit(self, parameter_list):
        raise NotImplementedError

class BatchEstimator:
    def __init__(self,
        estimator = None,
        df_screen = None,
        screen_batch_size = 25000
    ):
        indices_or_sections = [x for x in list(range(
            screen_batch_size,
            df_screen.shape[0],
            screen_batch_size
        ))]

        self.list_df_screen = np.split(
            df_screen,
            indices_or_sections = indices_or_sections,
            axis = 0
        )
        self.estimator = estimator
        for i in range(len(self.list_df_screen)):
            print(self.list_df_screen[i].shape)
            print(self.list_df_screen[i].columns)

    def predict(self, df):
        self.estimator.set_df_screen(self.list_df_screen[0])
        adjacency_matrix = self.estimator.predict(df.copy())
        adjacency_matrix = ExtraFields(
            df_screen = self.list_df_screen[0],
            adjacency_matrix = adjacency_matrix,
            df_party = df.copy(),
            score_factor = self.estimator.score_factor,
            threshold = self.estimator.threshold,
            key_party = self.estimator.key_party,
            key_screen = self.estimator.key_screen
        )
        print('first: ', adjacency_matrix.shape)
        for i in range(1,len(self.list_df_screen)):
            self.estimator.set_df_screen(self.list_df_screen[i])
            adjacency_matrix_ = self.estimator.predict(df)
            adjacency_matrix_ = ExtraFields(
                df_screen = self.list_df_screen[i],
                adjacency_matrix = adjacency_matrix_,
                df_party = df.copy(),
                score_factor = self.estimator.score_factor,
                threshold = self.estimator.threshold,
                key_party = self.estimator.key_party,
                key_screen = self.estimator.key_screen
            )
            print('second: ', adjacency_matrix.shape)
            adjacency_matrix = adjacency_matrix.append(
                adjacency_matrix_,
                ignore_index = True
            )
            print('third: ', adjacency_matrix.shape)
        return (adjacency_matrix)

    def fit(self, series):
        self.estimator.fit(series)