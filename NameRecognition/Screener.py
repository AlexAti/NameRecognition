class Screener():
    def __init__(self, screnning_list = None):
        self.screnning_list = screnning_list

    def screnning(self, df, field):
        df[field + '_threshold'] = 90.0
        return df

    def fit(self, parameter_list):
        raise NotImplementedError