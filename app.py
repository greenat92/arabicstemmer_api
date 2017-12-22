import os

from flask import Flask, Blueprint
from flask_restful import Api, output_json
from flask_jwt import JWT
from flask_cors import CORS

from security import authenticate, identity
from resources.user import UserRegister
from resources.word import Word, WordList
from resources.stem import Stem, StemList
from resources.stopwords import Stopword, StopwordList
from resources.stemmer import StemText

app = Flask(__name__)

app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '9&[!=l-n>;*{B@,N'
CORS(app)
api = Api(app)
# blueprint = Blueprint('api', __name__, url_prefix='/api/v1') # TODO: add url_prefix to api

jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Stem, '/v1/stem/<string:stem_value>')
api.add_resource(Word, '/v1/word/<string:word_value>')
api.add_resource(Stopword, '/v1/stopword/<string:stopword_value>')

api.add_resource(WordList, '/v1/words')
api.add_resource(StemList, '/v1/stems')
api.add_resource(StopwordList, '/v1/stopwords')

api.add_resource(StemText, '/v1/stem')

api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5000)
