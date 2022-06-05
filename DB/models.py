from base64 import encode
from enum import unique
from winreg import REG_LEGAL_OPTION
from tables import Col
from .SqlAlchemy import Base
from sqlalchemy import Column, ForeignKey,Integer,String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__="Users"
    id=Column(Integer,primary_key=True,nullable=False)
    firstName=Column(String,nullable=False)
    lastName=Column(String,nullable=False)
    email=Column(String,nullable=False,unique=True)
    phoneNumber=Column(String,nullable=False)
    password=Column(String,nullable=False)
    createdTime=Column(TIMESTAMP(timezone=False),nullable=False,server_default=text("now()"))


class Noun(Base):
    __tablename__="Nouns"
    id=Column(Integer,primary_key=True,nullable=False)
    artical=Column(String,nullable=False)
    noun=Column(String,nullable=False,unique=True)
    createdTime=Column(TIMESTAMP(timezone=False),nullable=False,server_default=text("now()"))

    
    

class EngDef(Base):
    __tablename__="EngDefinitions"
    id=Column(Integer,primary_key=True,nullable=False)
    definition=Column(String,nullable=False)
    noun_id=Column(Integer,ForeignKey("Nouns.id",ondelete="CASCADE"),nullable=False)
    createdTime=Column(TIMESTAMP(timezone=False),nullable=False,server_default=text("now()"))
    owner=relationship("Noun")
