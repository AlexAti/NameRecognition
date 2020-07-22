# Text mining
from sklearn.feature_extraction.text import CountVectorizer
# Expresiones regulares
import re
# Aplicacion de funciones recursivas
from functools import reduce
# Biblioteca ciencia de datos
import pandas as pd
# Biblioteca de paralelizado de apply
import swifter

class BaseTransformer:
    '''
    Transformador base para la implementación de transformadores sobre nombres.
    '''
    def __init__(self):
        raise NotImplementedError

    def transform(self, series):
        raise NotImplementedError

    def fit(self, series):
        raise NotImplementedError

class SNTransformer(BaseTransformer):
    '''
    Transformador de estandarización de nombres.
    '''
    def __init__(self):
        # Funcion optimizada de estandarizacion
        self.estandar_name = lambda s: re.sub(r'[^<\w\s]','',re.sub('\s+', ' ', str(s).lower()).strip())

    def transform(self, series):
        return(series.swifter.apply(self.estandar_name))

    def fit(self, series):
        pass

    def fit_transform(self,series):
        self.fit(series)
        return(self.transform(series))

class SWCTransformer(BaseTransformer):
    '''
    Transformador identificador y filtrador de StopWords.
    '''
    def __init__(self, threshold = 0.50, min_df = 0.05, max_word = 1000, exceptions = None):
        self.threshold = threshold
        # Declaramos las propiedades del contador de palabras
        self.word = CountVectorizer(
            # Pasar minuculas
            lowercase = True,
            # Tomar palabras en duos y trios tambien
            ngram_range = (1,3),
            # Dividir una frase en palabras
            analyzer = "word",
            # Minima aparicion en el corpus
            min_df = min_df,
            # Maximo de caracteristicas
            max_features = max_word,
            # Simplificamos el tokenizer para admitir todos los char
            tokenizer = lambda s: s.split(' '), # Posible mejora diferenciando mayus [A..Z] + [a..z]+
            # Eliminamos la expresion regular que define que es una palabra
            token_pattern = None,
            # Excepciones que no queremos que quite
            stop_words = exceptions
        )
        # Funcion de motor de filtro optimizado
        self.engine_filter = lambda name, stop_word: (' ' + name + ' ').replace(' ' + stop_word + ' ',' ')[1:-1]
        self.word_list = []

    def word_filter(self, series):
        series = series.swifter.apply(lambda name: reduce(self.engine_filter, [name] + self.word_list))
        return(series)

    def fit(self, series):
        try:
            self.word.fit(series)
            self.word_list = self.word.get_feature_names()
            self.word_list = sorted(self.word_list, key=len, reverse = True)
        except:
            pass

    def transform(self, series):
        series = self.word_filter(series)
        series = series.swifter.apply(lambda s: re.sub('\s+', ' ', s).strip())
        return(series)

    def fit_transform(self, series):
        self.fit(series)
        return (self.transform(series))