from fastapi import HTTPException, status,Depends,Response,APIRouter
from .. import schema,utils
from sqlalchemy.orm import Session
from DB.SqlAlchemy import get_db
from DB import models
from typing import List
from sqlalchemy.exc import IntegrityError



router=APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schema.UserOut)
def create_user(user:schema.UserModel,db: Session = Depends(get_db)):
    #first name, last name , phone number , email, password
    #userList.append(user.dict())
    try:
        #newUser=dbm.createUser(user)
        #newUser=models.User(firstName=user.firstName,lastName=user.lastName,email=user.email,phoneNumber=user.phoneNumber,password=user.password)
        user.password= utils.get_password_hash(user.password)
        newUser=models.User(**user.dict())
        db.add(newUser)
        db.commit()
        db.refresh(newUser)
        return newUser
    except IntegrityError as err:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail=str("User already Exist"))
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail=str(err))


@router.get("/",response_model=List[schema.AllUsers])
def get_users_list(db: Session = Depends(get_db)):
    Users=db.query(models.User).all()
    return Users
    #return dbm.selectUsers()

@router.get("/{id}",response_model=schema.UserOut)
def get_user(id:int,db: Session = Depends(get_db)):
    
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str("invalid user"))
    return user #dbm.selectUserById(id)

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_User(id:int,db: Session = Depends(get_db)):
    t_user=db.query(models.User).filter(models.User.id==id).first()
    print(t_user)
    if not t_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str("Not Found"))
    else:
        db.query(models.User).filter(models.User.id==id).delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.patch("/{id}")
def patch_user(id:int,user_data:schema.UpdateUser,db: Session = Depends(get_db)):
    User_Query=db.query(models.User).filter(models.User.id==id)
    if not User_Query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str("Not Found"))
    temp=User_Query.first()
    temp.firstName=user_data.firstName
    temp.lastName=user_data.lastName
    User_Query.update(user_data.dict(),synchronize_session=False)
    db.commit()
    return User_Query.first()