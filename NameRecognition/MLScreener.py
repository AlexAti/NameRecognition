from NameRecognition.Screener import Screener
from NameRecognition.CSChar import CSChar
from NameRecognition.StopWordClean import StopWordClean
import pandas as pd

class MLScreener(Screener):
    def __init__(self, 
        threshold = None, 
        score_factor = None,
        df_screen = None, 
        key_screen = None, 
        value_screen = None, 
        key_party = None, 
        value_party = None, 
        verbose = False
    ):
        self.SWC = StopWordClean(verbose = verbose)
        self.CSChar = CSChar(threshold = threshold['value_threshold'] / 100.0, verbose = True)
        self.df_screen = df_screen
        self.key_screen = key_screen
        self.value_screen = value_screen
        self.key_party = key_party
        self.value_party = value_party
        self.threshold = threshold
        self.score_factor = score_factor

    def fit(self, serie):
        serie_ = self.SWC.fit_clean(serie)
        self.CSChar.fit(serie_)
        self.df_screen['clean'] = self.SWC.clean(self.df_screen[self.value_screen])

    def screening(self, df, field = None):
        # Limpieza del nombre
        df['clean'] = self.SWC.clean(df[self.value_party])
        # Cotejo de nombre
        self.screen = self.CSChar.screen(
            df1 = self.df_screen,
            df2 = df,
            key1 = self.key_screen,
            key2 = self.key_party,
            value1 = 'clean',
            value2 = 'clean'
        )
        # Aplicación de los score_factor
        self.screen = pd.merge(
            left = self.screen,
            right = self.df_screen,
            how = 'left',
            on = self.key_screen
        ).rename({
            'birth_date': 'birth_date_screen',
            'birth_country': 'birth_country_screen',
            'identifier': 'identifier_screen'
        }, axis = 1)
        self.screen = pd.merge(
            left = self.screen,
            right = df,
            how = 'left',
            on = self.key_party
        ).rename({
            'birth_date': 'birth_date_party',
            'birth_country': 'birth_country_party',
            'identifier': 'identifier_party'
        }, axis = 1)
        # Calculo de la puntuación global
        self.screen['global_score'] = self.screen.apply(
            lambda row: 
                self.score_factor['birth_country_factor'] * (row['birth_country_party'] == row['birth_country_screen']) +
                self.score_factor['identifier_factor'] * (row['identifier_party'] == row['identifier_screen']) +
                row['score'] * 100
        , axis = 1)
        self.screen.drop(self.screen.columns.difference(
            ['key_screen','key_party','score','global_score']
        ), axis = 1, inplace = True)
        # Fitro puntuación global
        self.screen.drop(
            self.screen[self.screen['global_score'] < self.threshold['global_threshold']].index
        , axis = 0, inplace = True)
        # Filtro de aparicion
        ids = set(self.screen[self.key_party])
        df.drop(
            df[df[self.key_party].apply(lambda key: key not in ids)].index
        , inplace = True, axis = 0)
        # Calculo de score
        df = pd.merge(
            left = df,
            right = self.screen.groupby([self.key_party])['score'].max().reset_index(),
            how = 'inner',
            on = self.key_party
        )
        return df