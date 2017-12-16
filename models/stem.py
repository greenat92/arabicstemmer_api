from db import db

class StemModel(db.Model):
    __tablename__ = 'stems'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, unique=True, nullable=False)

    words = db.relationship('WordModel', lazy='dynamic')

    # def __unicode__(self):
    #     return u"%s. %s" % (self.id, self.text)

    def __init__(self, stem_value):
        self.text = stem_value

    # def __repr__(self):
    #     return '<text %r>' % self.text

    def json(self):
        return {'stem': self.text, 'words': [word.json() for word in self.words.all()]}

    @classmethod
    def find_by_stem(cls, stem_value):
        return cls.query.filter_by(text=stem_value).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
