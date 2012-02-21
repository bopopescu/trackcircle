from trackcircle.database import Base
from trackcircle.models import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship, backref
from datetime import datetime
import re
from trackcircle.config import AMAZON_S3_BUCKET
from time import time
from mutagen.easyid3 import EasyID3

class Track(Base, BaseModel):
    __tablename__ = 'tracks'
    id = Column(Integer, primary_key=True)
    created_time = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref=backref('tracks', lazy='dynamic'))
    keyname = Column(String(255))
    original_filename = Column(String(255))
    artist = Column(String(255))
    title = Column(String(255))
    year = Column(Integer)
    bpm = Column(Integer, default=0)
    artwork_url = Column(String(255))
    notes = Column(Text)
    
    def set_id3_by_file(self, sourcefile):
        tags = EasyID3(sourcefile)
        if tags:
            self.artist = tags.get('artist')[0] if tags.get('artist') else ''
            self.title = tags.get('title')[0] if tags.get('title') else ''
            self.year = int(tags.get('date')[0]) if tags.get('date') else 0
            self.bpm = int(tags.get('bpm')[0]) if tags.get('bpm') else 0
        
        
    def generate_keyname(self):
        strip_mp3 = re.sub(r'(\.mp3)|(\.MP3)', '', self.original_filename)
        convert_spaces = re.sub(r'\s+', '_', strip_mp3)
        alphanumericspace = re.sub(r'\W+', '', convert_spaces)
        final = 'trackcircle-dev/tracks/%s/%s-%s.mp3' % \
                (self.user_id, int(time()), alphanumericspace,)
        return final
        
    def __init__(self, user_id, original_filename, artist = '', title = '', notes = ''):
        self.created_time = datetime.utcnow()
        self.user_id = user_id
        self.original_filename = original_filename
        self.artist = artist
        self.title = title
        self.notes = notes
        self.keyname = self.generate_keyname()

    
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