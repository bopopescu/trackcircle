from trackcircle.database import Base
from trackcircle.models import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship, backref
from datetime import datetime


class User(Base, BaseModel):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    facebook_id = Column(Integer, unique=True)
    created_time = Column(DateTime)
    email = Column(String(128))
    facebook_info = None
    
    def __init__(self, facebook_id, email = ''):
        self.created_time = datetime.utcnow()
        self.facebook_id = facebook_id
        self.email = email
        
    
    def __repr__(self):
        return '<User %r, Facebook ID %r>' % (self.id, self.facebook_id,)