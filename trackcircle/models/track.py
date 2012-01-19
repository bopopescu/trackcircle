from trackcircle.database import Base
from trackcircle.models import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship, backref
from datetime import datetime
import boto
from trackcircle import bucket

class Track(Base, BaseModel):
    __tablename__ = 'tracks'
    id = Column(Integer, primary_key=True)
    created_time = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))
    url = Column(String(255))
    original_filename = Column(String(255))
    artist = Column(String(255))
    title = Column(String(255))
    notes = Column(String(255))
    
    def __init__(self, user_id, url, original_filename, artist = '', title = '', notes = ''):
        self.created_time = datetime.utcnow()
        self.user_id = user_id
        self.url = url
        self.original_filename = original_filename
        self.artist = artist
        self.title = title
        self.notes = notes
        
    
    def __repr__(self):
        return '<Track %s - %s (%r)>' % (self.artist, self.title, self.id,)
        
    def __str__(self):
        if self.artist == '' or self.title == '':
            return self.original_filename
        return "%s - %s" % (self.artist, self.title)
    
    @property 
    def s3_url(self):
        key = bucket.get_key(self.url)
        if key:
            return 'http://dev.monospectra.com/%s' % self.url
        return "#notfound"
        