from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.word import WordModel

class Word(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('stem_id',
        type=int,
        required=True,
        help="Every word needs a stem."
    )

    #@jwt_required()
    def get(self, word_value):
        word = WordModel.find_by_word(word_value)
        if word:
            return word.json()
        return {'message': 'Word not found'}, 404

    #@jwt_required()
    def post(self, word_value):
        if WordModel.find_by_word(word_value):
            return {'message': "An word with name '{}' already exists.".format(word_value)}, 400

        data = Word.parser.parse_args()

        word = WordModel(word_value, **data)

        try:
            word.save_to_db()
        except:
            return {"message": "An error occurred inserting the word."}, 500

        return word.json(), 201

    #@jwt_required()
    def delete(self, word_value):
        word = WordModel.find_by_word(word_value)
        if word:
            word.delete_from_db()

        return {'message': 'word deleted'}

    #@jwt_required()
    def put(self, word_value):
        data = Word.parser.parse_args()

        word = WordModel.find_by_word(word_value)

        if word is None:
            word = WordModel(word_value, **data)
        else:
            word.stem_id = data['stem_id']
            word.text = word_value

        word.save_to_db()

        return word.json()


class WordList(Resource):
    #@jwt_required()
    def get(self):
        return {'words': [x.json() for x in WordModel.query.all()]} # TODO: pagination
