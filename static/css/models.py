from sqlalchemy import Column,Integer,String,LargeBinary,DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Fingerprint(Base):

    __tablename__="fingerprints"

    id = Column(Integer, primary_key=True)

    name = Column(String)

    address = Column(String)

    image_path = Column(String)

    feature_vector = Column(LargeBinary)


class MatchHistory(Base):

    __tablename__="match_history"

    id = Column(Integer, primary_key=True)

    fingerprint_id = Column(Integer)

    matched_id = Column(Integer)

    score = Column(String)

    timestamp = Column(DateTime, default=datetime.utcnow)