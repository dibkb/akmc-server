from sqlalchemy import Column, Integer, String
from server.api.schemas import TableClassNames
from server.database.main import Base
from sqlalchemy.orm import  relationship
from passlib.hash import bcrypt

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), unique=True, nullable=False)
    refresh_token = Column(String(255),nullable=True)
    password_hash = Column(String(128),nullable=False)
    profilePic = Column(String,nullable=True)

    chats = relationship(TableClassNames.Chat.value, back_populates="user")
    messages = relationship(TableClassNames.Message.value, back_populates="user")


    def set_password(self, password: str):
        self.password_hash = bcrypt.hash(password)

    # Method to verify password
    def verify_password(self, password: str):
        return bcrypt.verify(password, self.password_hash)


