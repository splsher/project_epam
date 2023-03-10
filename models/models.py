from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
)

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from datetime import datetime

datetime.utcnow()

BaseModel = declarative_base()
metadata = BaseModel.metadata

mysql_engine = create_engine("mysql+pymysql://root:Bonia9977@localhost/social_network", echo=True,
                             future=True)


Session = sessionmaker(bind=mysql_engine)
session = Session()


class User(BaseModel):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(45), nullable=False)
    email = Column(String(45), nullable=False)
    password = Column(String(160), nullable=False)
    city = Column(String(40), nullable=False)
    photo = Column(String(250), nullable=True)


class Wall(BaseModel):
    __tablename__ = "wall"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'),
                     nullable=False)
    datetime = Column(DateTime, nullable=False, default=datetime.utcnow())
    title = Column(String(100), nullable=True)
    text = Column(String(500), nullable=False)
    photo_wall = Column(String(250), nullable=True)
