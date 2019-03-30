from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    nick = db.Column(db.String(50))
    password = db.Column(db.String(40))
    email = db.Column(db.String(100))

    def __repr__(self):
        return "<User(id='%s' nick='%s')>" % (self.id, self.nick)
