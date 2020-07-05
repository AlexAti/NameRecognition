from flask_restful import Resource, reqparse
from NameRecognition.app import screener

class OnDemand(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('key_party')
        parser.add_argument('value_party')
        args = parser.parse_args()
        print(args['key_party'])
        print(args['value_party'])
        df = pd.DataFrame([{
            'key_party': args['key_party'],
            'value_party': args['value_party'],
        }])
        df_filter = screener.screening(df)
        return {
            'df_filter': df_filter.to_dict(orient = 'list'),
            'screen': screener.screen.to_dict(orient = 'list')
        }