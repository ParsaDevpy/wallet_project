from sqlalchemy import Column,String,DateTime,Integer
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class database_wallet(Base):
    __tablename__ = "db wallet"

    username = Column(String,primary_key=True)
    email = Column(String)
    password = Column(String)
    fullname = Column(String)
    created_at = Column(DateTime,default= datetime.utcnow)
    last_login = Column(DateTime,default = datetime.utcnow)
