from trackcircle.database import Base
from trackcircle.models import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship, backref
from datetime import datetime
import re
from trackcircle.config import AMAZON_S3_BUCKET

class Track(Base, BaseModel):
    __tablename__ = 'tracks'
    id = Column(Integer, primary_key=True)
    created_time = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))
    keyname = Column(String(255))
    original_filename = Column(String(255))
    artist = Column(String(255))
    title = Column(String(255))
    notes = Column(String(255))
    
    def generatekeyname(self):
        strip_mp3 = re.sub(r'(\.mp3)|(\.MP3)', '', self.original_filename)
        convert_spaces = re.sub(r'\s+', '_', strip_mp3)
        alphanumericspace = re.sub(r'\W+', '', convert_spaces)
        final = 'trackcircle-dev/tracks/%s/%s.mp3' % (self.user_id, alphanumericspace,)
        return final
        
    def __init__(self, user_id, original_filename, artist = '', title = '', notes = ''):
        self.created_time = datetime.utcnow()
        self.user_id = user_id
        self.original_filename = original_filename
        self.artist = artist
        self.title = title
        self.notes = notes
        self.keyname = self.generatekeyname()
        # 01_** Cub//--_Keep_Shelly_In_Athens_Remix.mp3
    
    def __repr__(self):
        if self.artist == '' and self.title == '':
            return '<Track %s (%r)>' % (self.keyname, self.id,)
        else:
            return '<Track %s - %s (%r)>' % (self.artist, self.title, self.id,)
        
    def __str__(self):
        if self.artist == '' or self.title == '':
            return self.original_filename
        return "%s - %s" % (self.artist, self.title)
        
    @property 
    def url(self):
        if not self.keyname:
            self.keyname = self.generatekeyname(self.original_filename)
        return 'http://%s/%s' % (AMAZON_S3_BUCKET, self.keyname,)