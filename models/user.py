from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    nick = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    photo_profile = db.Column(db.String(40), unique=True, nullable=True)

    def __init__(self, name, nick, password, email, photo_profile=None, id=None):
        self.id = id
        self.name = name
        self.nick = nick
        self.password = password
        self.email = email
        self.photo_profile = photo_profile

    def __repr__(self):
        return "<User(id='%s' nick='%s')>" % (self.id, self.nick)
