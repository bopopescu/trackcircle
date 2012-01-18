from trackcircle.database import db_session

class BaseModel(object):
    __tablename__ = 'basemodels'
    
    def __init__(self):
        pass
    
    def __repr__(self):
        return '<BaseModel>'
        
    def create(self):
        db_session.add(self)
        db_session.commit()
        
    def save(self):
        self.create()
    
    def delete(self):
        db_session.delete(self)
        db_session.commit()