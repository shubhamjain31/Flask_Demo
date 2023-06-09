from sqlalchemy import TIMESTAMP, Column, String, Integer, DateTime, ForeignKey, Boolean, Text, JSON, Float
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import UUID
from flask_login import UserMixin

from core.database.connection import Base

import datetime, uuid
import passlib.hash as _hash

class BaseModel(Base):
    __abstract__ = True

    ip_address      = Column(String(255))
    user_agent      = Column(Text)

class User(BaseModel, Base, UserMixin):
    __tablename__ = "users"

    id              = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username        = Column(String, unique=True)
    email           = Column(String, unique=True, index=True)
    name            = Column(String(150))
    password        = Column(String(255))
    is_active       = Column(Boolean, default=True)
    is_superuser    = Column(Boolean, default=False)
    profile         = Column(String(255), nullable=True)
    date_created    = Column(DateTime, default=datetime.datetime.utcnow)

    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.password)
    
    def __repr__(self):
        return self.username
    
class Token(Base):
    __tablename__ = "token"

    id              = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email           = Column(String(100), unique=True)
    token           = Column(String(255))
    user_id         = Column(String(100))

    def __repr__(self):
        return self.email
    
class Post(BaseModel, Base):
    __tablename__ = "posts"

    id              = Column(Integer, primary_key=True, index=True)
    user_id         = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    post_name       = Column(String, unique=True, index=True)
    post_text       = Column(Text)
    created_at      = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at      = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    owner           = relationship("User", backref=backref("posts", uselist=False))

    def __repr__(self):
        return self.post_name 