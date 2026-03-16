from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Text, LargeBinary, DateTime, Boolean, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(UserMixin, Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Fingerprint(Base):
    __tablename__ = 'fingerprints'
    id = Column(Integer, primary_key=True)
    name = Column(String(120))
    address = Column(Text)
    image_path = Column(String(256))
    feature_vector = Column(LargeBinary)  # store raw bytes
    created_at = Column(DateTime, default=datetime.utcnow)

    matches = relationship('MatchHistory', back_populates='fingerprint')


class MatchHistory(Base):
    __tablename__ = 'match_history'
    id = Column(Integer, primary_key=True)
    fingerprint_id = Column(Integer, ForeignKey('fingerprints.id'))
    matched_id = Column(Integer)  # id of the matched fingerprint
    score = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

    fingerprint = relationship('Fingerprint', back_populates='matches')
