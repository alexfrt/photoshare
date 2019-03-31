from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    nick = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __init__(self, name, nick, password, email, id=None):
        self.id = id
        self.name = name
        self.nick = nick
        self.password = password
        self.email = email

    def __repr__(self):
        return "<User(id='%s' nick='%s')>" % (self.id, self.nick)
