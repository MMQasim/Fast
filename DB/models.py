from tables import Col
from .SqlAlchemy import Base
from sqlalchemy import Column,Integer,String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

class User(Base):
    __tablename__="Users"
    id=Column(Integer,primary_key=True,nullable=False)
    firstName=Column(String,nullable=False)
    lastName=Column(String,nullable=False)
    email=Column(String,nullable=False,unique=True)
    phoneNumber=Column(String,nullable=False)
    password=Column(String,nullable=False)
    createdTime=Column(TIMESTAMP(timezone=False),nullable=False,server_default=text("now()"))


