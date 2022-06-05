from datetime import datetime
from pydantic import BaseModel, validator,EmailStr
from email_validator import validate_email, EmailNotValidError
from fastapi import  HTTPException, status
import re


class Userlogin(BaseModel):
    
    email:EmailStr
    password:str

    @validator('email')
    def email_validation(cls,v):
        try:
            email = validate_email(v).email
            return email
        except EmailNotValidError as e:
            raise ValueError(str(e))

    


    class Config:
        orm_mode=True




class UserModel(Userlogin):
    firstName:str
    lastName:str
    phoneNumber:str
    #middelName:Optional[str]=None
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
    
    @validator('phoneNumber')
    def phoneNumber_validation(cls,v):
        validate_phone_number_pattern = "^\\+?[1-9][0-9]{7,14}$"
        if (re.match(validate_phone_number_pattern, v)):
            return v
        else:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail="Incorrect Phone Number")


class UserOut(BaseModel):
    firstName:str
    lastName:str

    class Config:
        orm_mode=True

class AllUsers(UserModel):
    id:int
    createdTime:datetime
    class Config:
        orm_mode=True

class UpdateUser(BaseModel):

    firstName:str
    lastName:str

    class Config:
        orm_mode=True
    
class Token(BaseModel):
    access_token: str
    token_type: str