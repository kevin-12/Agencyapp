from sqlalchemy import Column, Integer, String,Sequence
from .db import Base
from flask_login import UserMixin

#models for your database
class User(Base):
     __tablename__ = "users"
     id = Column(Integer, primary_key=True) 
     Username = Column(String(50), unique=True,nullable=False) 
     password = Column(String(120))
     email = Column(String(64))
    

     def __init__(self,Username=None,password=None, admin=None, email=None):
          self.Username = Username
          self.password=password
          self.email = email
          self.admin=admin

class Nanny(Base):
     __tablename__ = "nannies"
     id = Column(Integer, primary_key=True)
     Name=Column(String(50),nullable=False) 
     Username = Column(String(50), unique=True,nullable=False) 
     password = Column(String(120))
     email = Column(String(64))
     city=Column(String(50),nullable=False) 
     profile_picture=Column(String(64))
     summary=Column(String(255))
     curriculum=Column(String(50))

     def __init__(self,Name=None,Username=None,password=None, email=None,city=None,summary=None , curriculum=None,profile_picture=None):
          self.Name=Name
          self.Username = Username
          self.password=password
          self.email = email
          self.city=city
          self.profile_picture=profile_picture
          self.summary=summary
          self.curriculum= curriculum

class BookedNanny(Base):
     __tablename__ = "booked_nannies"
     id = Column(Integer, primary_key=True) 
     Name=Column(String(50),nullable=False) 
     Username = Column(String(50),nullable=False) 
     email = Column(String(64))
     city=Column(String(50),nullable=False) 

     def __init__(self,Name=None,Username=None, email=None,city=None):
          self.Name=Name
          self.Username = Username
          self.email = email
          self.city=city
          
      

     