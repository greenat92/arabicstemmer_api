from db import db

class StopwordModel(db.Model):
    __tablename__ = 'stopwords'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, unique=True, nullable=False)

    # def __unicode__(self):
    #     return u"%s. %s" % (self.id, self.text)

    def __init__(self, stopword):
        self.text = stopword

    # def __repr__(self):
    #     return '<text %r>' % self.text

    def json(self):
        return {'stopword': self.text }

    @classmethod
    def find_by_stopword(cls, stopword):
        return cls.query.filter_by(text=stopword).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
