from sqlalchemy import Column, Integer, String
from server.api.schemas import TableClassNames
from server.database.main import Base
from sqlalchemy.orm import  relationship
from passlib.hash import bcrypt

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(128),nullable=True)
    profilePic = Column(String,nullable=True)

    chats = relationship(TableClassNames.Chat.value, back_populates="user")
    messages = relationship(TableClassNames.Message.value, back_populates="user")

class Oauth(Base):
    __tablename__ = "oauth"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), unique=True, nullable=False)
    profilePic = Column(String,nullable=True)

    chats = relationship(TableClassNames.Chat.value, back_populates="oauth")
    
    messages = relationship(TableClassNames.Message.value, back_populates="oauth")


