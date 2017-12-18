from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from arabicstemmer import ArabicStemmer
from pyarabic.araby import tokenize
from helpers.stops import STOPS_LIST
from models.stem import StemModel
from models.word import WordModel

# TODO: strip ponctuation marks using Regx
# TODO: filter stopwords
# TODO: store stem/words in the db
class StemText(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('text',
        type=str,
        required=True,
        help="Arabic Text to be stemmed."
    )
    #@jwt_required()
    def post(self):
        data = StemText.parser.parse_args()
        if len(data['text']) == 0:
            return {"messgae": "This field cannot be blank"}
        else:
            tokens = tokenize(data['text'])
            stemmer = ArabicStemmer()
            stems = []
            result = {'stem': '', 'words': []}
            stop_nbr = 0
            for token in tokens: # TODO: improve this block by using python list comprehension
                token = token.strip()
                if token in STOPS_LIST:
                    stemmed = token
                    stop_nbr += 1
                else:
                    stemmed = stemmer.stemWord(token)
                i = 0
                found = False
                while (i < len(stems)):
                    if stems[i]['stem'] == stemmed:
                        stems[i]['words'].append(token)
                        found = True
                        break
                    i += 1

                if not found:
                    result['words'].append(token)
                    result['stem'] = stemmed
                    stems.append(result)
                    result = {'stem': '', 'words': []}
            return { "stems": stems,
                     "statistics":{"stems_count": len(stems),
                                   "words_count":len(tokens),
                                   "stops_count": stop_nbr,
                                   "ratio": len(stems)/float(len(tokens)) # TODO: redefine the ratio arithmetic
                                   }
                   }, 200
