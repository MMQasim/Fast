
from email import message
from sqlalchemy.exc import IntegrityError
from msilib.schema import Error
from typing import Optional
from fastapi import Body, FastAPI, HTTPException, status,Depends
from pydantic import BaseModel, validator
from email_validator import validate_email, EmailNotValidError
import re
from DB import dbManager as DBM
import time
from DB import models
from DB.SqlAlchemy import engine,get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)



host="localhost" 
database="fastDb"
password="123456"
user="postgres"

while True:
    dbm=DBM.DbManager(host=host,dbName=database,password=password,user=user)
    if dbm.connected:
        print("DB Connected")
        break

    time.sleep(3)




app = FastAPI()

userList=[]

class UserModel(BaseModel):
    firstName:str
    lastName:str
    email:str
    phoneNumber:str
    password:str
    middelName:Optional[str]=None
    
    @validator('firstName')
    def firstName_must_have_alphabet(cls, v):
        if not v.isalpha():
            raise ValueError('First name can only have alphabets')
        return v.title()

    @validator('lastName')
    def lastName_must_have_alphabet(cls, v):
        if not v.isalpha():
            raise ValueError('last name can only have alphabets')
        return v.title()

    @validator('email')
    def email_validation(cls,v):
        try:
            email = validate_email(v).email
            return email
        except EmailNotValidError as e:
            raise ValueError(str(e))

    @validator('phoneNumber')
    def phoneNumber_validation(cls,v):

        validate_phone_number_pattern = "^\\+?[1-9][0-9]{7,14}$"

        if (re.match(validate_phone_number_pattern, v)):
            return v
        else:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail="Incorrect Phone Number")
            


@app.get("/sql")
def test(db: Session = Depends(get_db)):
    temp=db.query(models.User).all()
    return{"data":temp}

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/users",status_code=status.HTTP_201_CREATED)
def sign_up(user:UserModel,db: Session = Depends(get_db)):
    #first name, last name , phone number , email, password
    #userList.append(user.dict())
    try:
        #newUser=dbm.createUser(user)
        newUser=models.User(firstName=user.firstName,lastName=user.lastName,email=user.email,phoneNumber=user.phoneNumber,password=user.password)
        db.add(newUser)
        db.commit()
        db.refresh(newUser)
        return newUser
    except IntegrityError as err:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail=str("User already Exist"))
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail=str(err))


@app.get("/users")
def get_users_list(db: Session = Depends(get_db)):
    Users=db.query(models.User).all()
    return {"Users":Users}
    return dbm.selectUsers()

@app.get("/users/{id}")
def get_user(id:int):
    try:
        return dbm.selectUserById(id)
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(err))