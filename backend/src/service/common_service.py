from src.config import *
from src.model.person import *
from src.model.car import *

# https://stackoverflow.com/questions/73837260/using-kwargs-with-filter-by-sqlalchemy
# https://medium.com/@nadiaaoliverr/o-que-significa-args-e-kwargs-em-python-d18a4120b744

# --- create

def create_object(m_class, **kwargs):
    obj = m_class(**kwargs)
    db.session.add(obj)
    db.session.commit()
    db.session.refresh(obj) # to get the id after creation
    return obj

# --- get

def get_objects(m_class):
    return db.session.query(m_class).all()
        
def get_object_by_attribute(m_class, attribute, value):
    return db.session.query(m_class).filter(getattr(m_class, attribute) == value).first()

# --- delete

def delete_object_by_id(m_class, object_id):
    try:
        obj = db.session.query(m_class).filter(m_class.id == object_id).first()
        db.session.delete(obj)
        db.session.commit()    
        return True    
    except:
        return False
    
# delete by the object itself
def delete_object(obj):
    try:
        db.session.delete(obj)
        db.session.commit()
        return True    
    except:
        return False