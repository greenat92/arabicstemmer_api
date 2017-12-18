from flask_restful import Resource, reqparse
from models.stopwords import StopwordModel

class Stopword(Resource):
    #@jwt_required()
    def get(self, stopword_value):
        stopword = StopwordModel.find_by_stopword(stopword_value)
        if stopword:
            return stopword.json()
        return {'message': 'stopword not found'}, 404

    #@jwt_required()
    def post(self, stopword_value):
        if StopwordModel.find_by_stopword(stopword_value):
            return {'message': "A stopword with name '{}' already exists.".format(stopword_value)}, 400

        stopword = StopwordModel(stopword_value)
        try:
            stopword.save_to_db()
        except:
            return {"message": "An error occurred creating the stopword."}, 500

        return stopword.json(), 201

    #@jwt_required()
    def delete(self, stopword_value):
        stopword = StopwordModel.find_by_stopword(stopword_value)
        if stopword:
            stopword.delete_from_db()

        return {'message': 'stopword deleted'}

    #@jwt_required()
    def put(self, stopword_value):

        stopword = StopwordModel.find_by_stopword(stopword_value)

        if stopword is None:
            stopword = WordModel(stopword_value)
        else:
            stopword.text = stopword_value

        stopword.save_to_db()

        return stopword.json()

class StopwordList(Resource):
    #@jwt_required()
    def get(self):
        return {'stopwords': [stopword.json() for stopword in StopwordModel.query.all()]} # TODO: pagination
