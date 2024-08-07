from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = 'User'

    username = Column(String, primary_key=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)

    posts = relationship('Post', back_populates='owner')


class Followers(Base):

    __tablename__="Followers"
    id=Column(Integer,primary_key=True)
    follower_username= Column(String, ForeignKey('User.username'), nullable=False)
    following_username = Column(String, ForeignKey('User.username'), nullable=False)

    follower = relationship('User', foreign_keys=[follower_username])
    following = relationship('User', foreign_keys=[following_username])

class Post(Base):

    __tablename__='Post'
    id=Column(Integer,primary_key=True,index=True)
    content= Column(String)
    user_username =Column(Integer,ForeignKey('User.username'))
    date_created = Column(DateTime, default=datetime.now)
    date_stored = Column(DateTime, default=datetime.now)

    owner = relationship("User", back_populates="posts")