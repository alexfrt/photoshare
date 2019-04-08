from flask.json import JSONEncoder
from models.user import User

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            return {
                'id': obj.id,
                'name': obj.name, 
                'nick': obj.nick,
                'email': obj.email,
                'photo_profile': obj.photo_profile if obj.photo_profile else 'empty.png'
            }
        return super(CustomJSONEncoder, self).default(obj)