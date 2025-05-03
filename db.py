from sqlalchemy import Column, Integer, String, DateTime, create_engine
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
 
class Static(Base):
    __tablename__ = "static"
    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=False) 
    timestamp = Column(DateTime, default=datetime.utcnow)

DB_URL="your DB_URL"
engine = create_engine(DB_URL, echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()
