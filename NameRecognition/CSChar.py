# Distancia empleada entre nombres
from sklearn.metrics.pairwise import cosine_similarity
# Text mining
from sklearn.feature_extraction.text import TfidfVectorizer
# Pipeline
from sklearn.pipeline import Pipeline
# Biblioteca ciencia de datos
import pandas as pd

class CSChar:
    def __init__(self, 
        threshold = 0.86, 
        ngram_range = (1,5), 
        max_df = 0.7,
        max_features = 60000,
        verbose = False):

        self.feature_extractor = TfidfVectorizer(
            # Pasar minuculas
            lowercase = True,
            # Tomar palabras en duos y trios tambien
            ngram_range = ngram_range,
            # Dividir una frase en palabras
            analyzer = "char_wb",
            # Maxima aparicion en el corpus
            max_df = max_df,
            # Maximo de caracteristicas
            max_features = max_features,
            # Decodificación
            decode_error = 'ignore',
            # Normalizacion l2 suma de los cuadrados del vector
            norm = "l2",
            # Frecuencia de documentos inversa
            use_idf = True,
            # Alisado de documentos
            smooth_idf = True,
            # Escala sublinear no usada
            sublinear_tf = False
        )
        self.threshold = threshold
        self.verbose = verbose

    def fit(self, serie):
        self.feature_extractor.fit(serie)

    def screen(self, df1, df2, key1, key2, value1, value2):
        # similitud coseno sobre matriz dispersa
        result = cosine_similarity(
            X = self.feature_extractor.transform(df1[value1].astype(str)),
            Y = self.feature_extractor.transform(df2[value2].astype(str)),
            dense_output = False
        )
        # Aplicamos el filtro
        result.data[result.data < self.threshold] = 0
        result.eliminate_zeros()
        df = pd.DataFrame(
            list(zip(*result.nonzero(), result.data)),
            columns = [key1, key2, 'score']
        )
        df[key1] = df1.reset_index(drop = True).loc[df[key1],key1].reset_index(drop = True)
        df[key2] = df2.reset_index(drop = True).loc[df[key2],key2].reset_index(drop = True)
        return df

if __name__ == "__main__":
    CSC = CSChar()

    df1 = pd.DataFrame(
        columns = ['Texto', 'Clave']
    )
    df1 = df1.append({'Texto': 'Hola tal', 'Clave': 0}, ignore_index=True)
    df1 = df1.append({'Texto': 'Hola que tal', 'Clave': 1}, ignore_index=True)
    df1 = df1.append({'Texto': 'Hola que tal estas ', 'Clave': 2}, ignore_index=True)
    df1 = df1.append({'Texto': 'Hola que tal yo bien', 'Clave': 3}, ignore_index=True)
    df1 = df1.append({'Texto': 'Hola hola que tal', 'Clave': 4}, ignore_index=True)
    df1 = df1.append({'Texto': 'hola que tal', 'Clave': 5}, ignore_index=True)
    df1 = df1.append({'Texto': 'Hola la que tal', 'Clave': 6}, ignore_index=True)
    df1 = df1.append({'Texto': 'Hola ola que tal', 'Clave': 7}, ignore_index=True)
    df1 = df1.append({'Texto': 'Hola ola que tal es', 'Clave': 8}, ignore_index=True)
    df1 = df1.append({'Texto': 'Hola ola tal no', 'Clave': 9}, ignore_index=True)
    df1 = df1.append({'Texto': 'Hola ola tal no Ernesto tal', 'Clave': 10}, ignore_index=True)
    df1 = df1.append({'Texto': 'Hola tal', 'Clave': 11}, ignore_index=True)
    df1 = df1.append({'Texto': 'Hola que tal', 'Clave': 12}, ignore_index=True)
    df1 = df1.append({'Texto': 'Hola que que tal estas ', 'Clave': 13}, ignore_index=True)
    df1 = df1.append({'Texto': 'Hola que tal yo bien', 'Clave': 14}, ignore_index=True)
    df1 = df1.append({'Texto': 'Hola hola que tal', 'Clave': 15}, ignore_index=True)
    df1 = df1.append({'Texto': 'hola que tl', 'Clave': 16}, ignore_index=True)
    df1 = df1.append({'Texto': 'Hola la que tal', 'Clave': 17}, ignore_index=True)
    df1 = df1.append({'Texto': 'Hola ola que tal', 'Clave': 18}, ignore_index=True)
    df1 = df1.append({'Texto': 'ola ola que tal es', 'Clave': 19}, ignore_index=True)
    df1 = df1.append({'Texto': 'Hola la tal no', 'Clave': 20}, ignore_index=True)
    df1 = df1.append({'Texto': 'Hola ola tal no Ernesto tal', 'Clave': 21}, ignore_index=True)
    df1 = df1.append({'Texto': 'Ernesto Martinez Pino', 'Clave': 22}, ignore_index=True)

    df1 = df1.rename({'Clave': 'Clave1'}, axis = 1)

    df2 = pd.DataFrame(
        columns = ['Texto', 'Clave']
    )
    df2 = df2.append({'Texto': 'Hola que tal estas', 'Clave': 0}, ignore_index=True)
    df2 = df2.append({'Texto': 'Hola tal como estas', 'Clave': 1}, ignore_index=True)
    df2 = df2.append({'Texto': 'Hola que tu', 'Clave': 2}, ignore_index=True)
    df2 = df2.append({'Texto': 'Hola que tu', 'Clave': 3}, ignore_index=True)
    df2 = df2.append({'Texto': 'Hola que tu es', 'Clave': 4}, ignore_index=True)
    df2 = df2.append({'Texto': 'Hola que tu que tal Ernesto', 'Clave': 5}, ignore_index=True)
    df2 = df2.append({'Texto': 'Hola que tal yo bien', 'Clave': 6}, ignore_index=True)
    df2 = df2.append({'Texto': 'Hola hola que tal', 'Clave': 7}, ignore_index=True)
    df2 = df2.append({'Texto': 'hola que tl', 'Clave': 8}, ignore_index=True)
    df2 = df2.append({'Texto': 'Hola la qe tal', 'Clave': 9}, ignore_index=True)
    df2 = df2.append({'Texto': 'Hola ola que al', 'Clave': 10}, ignore_index=True)
    df2 = df2.append({'Texto': 'ola ola que tal es', 'Clave': 11}, ignore_index=True)
    df2 = df2.append({'Texto': 'Hola la tal no', 'Clave': 12}, ignore_index=True)
    df2 = df2.append({'Texto': 'Hola ola tal no Eresto tal', 'Clave': 13}, ignore_index=True)
    df2 = df2.append({'Texto': 'Ernesto Martinez del Pino', 'Clave': 14}, ignore_index=True)
    df2 = df2.rename({'Clave': 'Clave2'}, axis = 1)

    CSC.fit(pd.concat(
        [df1['Texto'].astype(str),df2['Texto'].astype(str)]
    , axis = 0))

    s = CSC.screen(df1, df2, key1 = 'Clave1', key2 = 'Clave2', value1 = 'Texto', value2 = 'Texto')
    print(s)
