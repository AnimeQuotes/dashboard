from datetime import datetime

from mongoengine import *


class User(Document):
    username = StringField(required=True)
    password = StringField(required=True)
    created = DateTimeField(default=datetime.utcnow)
    is_admin = BooleanField(default=False)
    last_seen = DateTimeField()


class Character(Document):
    name = StringField(required=True)
    anime = StringField(required=True)
    added = DateTimeField(default=datetime.utcnow)
    author = ReferenceField(User, required=True)


class Image(Document):
    path = StringField(required=True, unique=True)
    date = DateTimeField(default=datetime.utcnow)
    character = ReferenceField(Character, required=True)
    uploader = ReferenceField(User, required=True)
