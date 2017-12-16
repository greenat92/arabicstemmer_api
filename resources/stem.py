from flask_restful import Resource, reqparse
from models.stem import StemModel

class Stem(Resource):
    def get(self, stem_value):
        stem = StemModel.find_by_stem(stem_value)
        if stem:
            return stem.json()
        return {'message': 'Stem not found'}, 404

    def post(self, stem_value):
        if StemModel.find_by_stem(stem_value):
            return {'message': "A stem with name '{}' already exists.".format(stem_value)}, 400

        stem = StemModel(stem_value)
        try:
            stem.save_to_db()
        except:
            return {"message": "An error occurred creating the stem."}, 500

        return stem.json(), 201

    def delete(self, stem_value):
        stem = StoreModel.find_by_stem(stem_value)
        if stem:
            stem.delete_from_db()

        return {'message': 'Stem deleted'}

    def put(self, stem_value):

        stem = StemModel.find_by_stopword(stopword_value)

        if stem is None:
            stem = StemModel(stem_value)
        else:
            stem.text = stem_value

        stem.save_to_db()

        return stem.json()

class StemList(Resource):
    def get(self):
        return {'stems': [stem.json() for stem in StemModel.query.all()]} # TODO: pagination
