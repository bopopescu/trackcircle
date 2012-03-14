from trackcircle.database import Base
from trackcircle.models import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref
from datetime import datetime
import re
from time import time

class Comment(Base, BaseModel):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    created_time = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref=backref('comments', lazy='dynamic'))
    track_id = Column(Integer, ForeignKey('tracks.id'))
    track = relationship('Track', backref=backref('comments', lazy='dynamic'))
    approved = Column(Boolean)
    spam = Column(Boolean)
    rating = Column(Integer)
    comment = Column(String(255))
    
    def __init__(self, track_id, user_id, comment):
        self.created_time = datetime.utcnow()
        self.user_id = user_id
        self.track_id = track_id
        self.comment = comment
        self.spam = False
        self.rating = 0
        self.approved = True
    
    def __repr__(self):
        return '<Comment on Track %r by User %r>' % (self.track_id, self.user_id,)
        
    @property
    def prettytime(self):
        format = None
        if not format:
            # Monday, January 1 2012
            format = "%A, %B %d %Y"
        return self.created_time.strftime(format)