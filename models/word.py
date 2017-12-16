from db import db

class WordModel(db.Model):
    __tablename__ = 'words'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, unique=True, nullable=False)

    stem_id = db.Column(db.Integer, db.ForeignKey('stems.id'))
    stem = db.relationship('StemModel')

    # def __unicode__(self):
    #     return u"%s. %s" % (self.id, self.text)

    def __init__(self, word, stem_id):
        self.text = word
        self.stem_id = stem_id

    # def __repr__(self):
    #     return '<text %r>' % self.text

    def json(self):
        return {'word': self.text, 'stem_id': self.stem_id } # TODO: get the value of the stem

    @classmethod
    def find_by_word(cls, word):
        return cls.query.filter_by(text=word).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
