class Pipeline:
    '''
    Tubería para encadenar transformaciones textuales.
    '''
    def __init__(self, transform_list):
        self.transform_list = transform_list

    def fit(self, series):
        for transformer in self.transform_list:
            series = transformer.fit_transform(series)

    def transform(self, series):
        for transformer in self.transform_list:
            series = transformer.transform(series)
        return(series)

    def fit_transform(self, series):
        self.fit(series)
        return(self.transform(series))