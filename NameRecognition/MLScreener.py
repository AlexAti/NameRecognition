from NameRecognition.Screener import Screener
from NameRecognition.CSChar import CSChar
from NameRecognition.StopWordClean import StopWordClean
import pandas as pd

class MLScreener(Screener):
    def __init__(self, threshold = None, df_screen = None, key_screen = None, value_screen = None, key_party = None, value_party = None, verbose = False):
        self.SWC = StopWordClean(verbose = verbose)
        self.CSChar = CSChar(threshold = threshold, verbose = True)
        self.df_screen = df_screen
        self.key_screen = key_screen
        self.value_screen = value_screen
        self.key_party = key_party
        self.value_party = value_party
        self.threshold = threshold

    def fit(self, serie):
        serie_ = self.SWC.fit_clean(serie)
        self.CSChar.fit(serie_)
        self.df_screen['clean'] = self.SWC.clean(self.df_screen[self.value_screen])

    def screening(self, df, field = None):
        df['clean'] = self.SWC.clean(df[self.value_party])
        self.screen = self.CSChar.screen(
            df1 = self.df_screen,
            df2 = df,
            key1 = self.key_screen,
            key2 = self.key_party,
            value1 = 'clean',
            value2 = 'clean'
        )
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