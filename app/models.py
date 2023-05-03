from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, text, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    mail = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_time = Column(DateTime(timezone=True), nullable=False, default=func.now())


class IPLog(Base):
    __tablename__ = 'ip_log'

    id = Column(Integer, primary_key=True, nullable=False)
    user_mail = Column(String, index=True, nullable=False)
    user_browser = Column(String, index=True, nullable=False)
    user_os = Column(String, index=True, nullable=False)
    user_device = Column(String, index=True, nullable=False)
    created_time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))


class URL(Base):
    __tablename__ = 'generated_urls'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, index=True, nullable=False)
    url = Column(String, index=True, nullable=False)
    shorten_url = Column(String, index=True, nullable=False)
    created_time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")


class URLLog(Base):
    __tablename__ = 'url_Log'

    id = Column(Integer, primary_key=True, nullable=False)
    user_mail = Column(String, index=True, nullable=False)
    user_browser = Column(String, index=True, nullable=False)
    user_os = Column(String, index=True, nullable=False)
    user_device = Column(String, index=True, nullable=False)
    created_time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))
    # owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    # owner = relationship("User")