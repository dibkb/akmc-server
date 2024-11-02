import enum
from sqlalchemy.sql import func
from sqlalchemy import Column, DateTime, ForeignKey, String,Integer,Enum,Text
from sqlalchemy.orm import  relationship

from server.api.schemas import TableClassNames
from server.database.main import Base

class RoleType(enum.Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class Chat(Base):
    __tablename__ = 'chats'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=True)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    oauth_id = Column(Integer, ForeignKey('oauth.id'), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship(TableClassNames.User.value, back_populates="chats")
    oauth = relationship(TableClassNames.Oauth.value, back_populates="chats")
    messages = relationship(TableClassNames.Message.value, back_populates="chat", order_by="Message.created_at")


class Message(Base):
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey('chats.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    oauth_id = Column(Integer, ForeignKey('oauth.id'), nullable=False)
    role = Column(Enum(RoleType), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    chat = relationship(TableClassNames.Chat.value, back_populates="messages")
    user = relationship(TableClassNames.User.value, back_populates="messages")
    oauth = relationship(TableClassNames.Oauth.value, back_populates="messages")