from trackcircle.database import Base
from trackcircle.models import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from pprint import pprint
from flaskext.oauth import OAuth

class User(Base, BaseModel):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    facebook_id = Column(Integer, unique=True)
    created_time = Column(DateTime)
    first_name = Column(String(255))
    last_name = Column(String(255))
    name = Column(String(255))
    username = Column(String(255))
    facebook_link = Column(String(255))
    facebook_picture = Column(String(255))
    timezone = Column(Integer)
    email = Column(String(128))
    facebook_info = None
    
    def __init__(self, facebook_id):
        self.created_time = datetime.utcnow()
        self.facebook_id = facebook_id
        
    def __repr__(self):
        return '<User %r, Facebook ID %r>' % (self.id, self.facebook_id,)
    
    
    def facebook_update(self, facebook):
        resp = facebook.get('/me')
        data = resp.data
        self.email = data['email']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.name = data['name']
        self.username = data['username']
        self.facebook_link = data['link']
        self.timezone = data['timezone']
        #print '/%s/picture?type=square' % self.username
        #resp = facebook.get('/me/picture')
        #pprint(resp.data)

        