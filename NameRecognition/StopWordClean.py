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

class StopWordClean:
    def __init__(self, threshold = 0.50, min_df = 0.05, max_word = 1000, exceptions = None, copy = True, verbose = False):
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
        # Acumulador de palabras
        self.word_list = []
        # Numero de fits
        self.nfit = 0
        # Mensajes
        self.verbose = verbose
        # Funcion de motor de filtro optimizado
        self.engine_filter = lambda name, stop_word: ((' ' + name + ' ').replace(' ' + stop_word + ' ',' ')[1:-1]) if (float(len((' ' + name + ' ').replace(' ' + stop_word + ' ',' ')[1:-1])) / float(len(name)) >= self.threshold) else name
        # Funcion optimizada de estandarizacion
        self.estandar_name = lambda s: re.sub(r'[^\w\s]','',re.sub('\s+', ' ', str(s).lower()).strip())
        # Clean no altera objeto serie
        self.copy = copy

    def standard_names(self, serie):
        serie = serie.swifter.apply(self.estandar_name)
        return(serie)

    def word_filter(self, serie):
        serie = serie.swifter.apply(lambda name: reduce(self.engine_filter, [name] + self.word_list))
        serie = serie.swifter.apply(lambda name: reduce(self.engine_filter, [name] + self.word_list))
        return(serie)

    def fit(self, serie):
        # Estandarizamos los datos
        serie_ = self.standard_names(serie.copy())
        if self.verbose: print("standard_names")
        # Entrenamos el vocabolario para el set
        try:
            self.word.fit(serie_)
            if self.verbose: print("vocabulary fit")
            self.word_list += self.word.get_feature_names()
        except:
            pass
        # Heuristica de orden
        self.word_list = sorted(self.word_list, key=len, reverse = True)
        if self.verbose == True: print(self.word_list)
        # Numero de fits
        self.nfit += 1

    def clean(self, serie):
        serie_ = None
        if self.copy:
            serie_ = serie.copy()
        else:
            serie_ = serie
        # Estandarizamos los datos
        serie_ = self.standard_names(serie_)
        if self.verbose: print("standard_names")
        # Realizamos el filtro de palabras sobre el set de datos
        serie_ = self.word_filter(serie_)
        if self.verbose: print("word filter")
        # Relimpiamos espacios
        serie_ = serie_.swifter.apply(lambda s: re.sub('\s+', ' ', s).strip())
        if self.verbose: print("clean spaces")
        # Devolvemos el set tras la limpieza
        return(serie_)

    def fit_clean(self, serie):
        self.fit(serie)
        return self.clean(serie)

    def intersection(self):
        # Distribucion de palabras
        values = pd.Series(self.word_list).value_counts()
        # Objecto serie
        word_list = pd.Series(self.word_list)
        # Interseccion de conjuntos
        self.word_list = list(set(word_list[word_list.apply(lambda x: True if values[x] == self.nfit else False)].tolist()))
        # Heuristica de orden
        self.word_list = sorted(self.word_list, key=len, reverse = True)