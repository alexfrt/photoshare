from app import db

association_table = db.Table(
    'photo_likes',
    db.Column('photo', db.String(36), db.ForeignKey('photo.uuid', ondelete='cascade'), nullable=False),
    db.Column('user', db.String(50), db.ForeignKey('user.nick', ondelete='cascade'), nullable=False)
)


class Photo(db.Model):
    uuid = db.Column(db.String(36), primary_key=True)
    user = db.Column(db.String(50), db.ForeignKey('user.nick', ondelete='cascade'))
    description = db.Column(db.String(50))
    when = db.Column(db.DateTime, nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)
    likes = db.relationship("User", secondary=association_table)
    did_like = False

    def __init__(self, uuid, user, description, when, data):
        self.uuid = uuid
        self.user = user
        self.description = description
        self.when = when
        self.data = data
        self.did_like = False

    def __repr__(self):
        return "<Photo(uuid='%s' when='%s')>" % (self.uuid, self.when)
