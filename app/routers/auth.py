from fastapi import HTTPException, status,Depends,Response,APIRouter
from .. import schema,utils,oauth2
from sqlalchemy.orm import Session
from DB.SqlAlchemy import get_db
from DB import models



router=APIRouter(
    prefix="/login",
    tags=["Auth"]
)

@router.post("/",response_model=schema.Token)
def login(user_data:schema.Userlogin,db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==user_data.email).first()
    try:
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
        if not utils.verify_password(user_data.password,user.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
        
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")

    access_token=oauth2.create_access_token(data={"email":user.email,"id":user.id})

    return {"access_token":access_token,"token_type": "bearer"}
    