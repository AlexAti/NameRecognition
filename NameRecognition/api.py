from flask_restful import Resource, reqparse
import pandas as pd

class OnDemand(Resource):
    def __init__(self, screener):
        self.screener = screener
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('key_party')
        self.parser.add_argument('value_party')
        self.parser.add_argument('birth_date')
        self.parser.add_argument('birth_country')
        self.parser.add_argument('identifier')

    def get(self):
        args = self.parser.parse_args()
        print(args['key_party'])
        print(args['value_party'])
        df = pd.DataFrame([{
            'key_party': args['key_party'],
            'value_party': args['value_party'],
            'birth_date': args['birth_date'],
            'birth_country': args['birth_country'],
            'identifier': args['identifier'],
        }])
        df_filter = self.screener.screening(df)
        return {
            'df_filter': df_filter.to_dict(orient = 'list'),
            'screen': self.screener.screen.to_dict(orient = 'list')
        }

class Screening(Resource):
    def __init__(self, screener):
        self.screener = screener
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('url')
        self.parser.add_argument('query')
    
    def get(self):
        args = self.parser.parse_args()
        print(args['url'])
        print(args['query'])
        from sqlalchemy import create_engine
        conn = create_engine(args['url'])
        df = pd.read_sql_query(
            con = conn,
            sql = args['query'],
            index_col = None
        )
        df_filter = self.screener.screening(df)
        return {
            'df_filter': df_filter.to_dict(orient = 'list'),
            'screen': self.screener.screen.to_dict(orient = 'list')
        }


    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('value_threshold')
        self.parser.add_argument('global_threshold')

    def get(self):
        args = self.parser.parse_args()