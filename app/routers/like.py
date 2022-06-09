from email import message
from fastapi import HTTPException, status,Depends,Response,APIRouter
from .. import schema,utils,oauth2
from sqlalchemy.orm import Session
from DB.SqlAlchemy import get_db
from DB import models
from typing import List
from sqlalchemy.exc import IntegrityError



router=APIRouter(
    prefix="/likes",
    tags=["Likes"]
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model={})
def liked_post(like_noun:schema.Like_in,db: Session = Depends(get_db), c_user:schema.AllUsers =Depends(oauth2.get_current_user)):
    check=db.query(models.Like).filter(models.Like.noun_id==like_noun.noun_id,models.Like.user_id==c_user.id)
    noun=db.query(models.Noun).filter(models.Noun.id==like_noun.noun_id).first()
    if like_noun.dir:
        if not check.first():
            if not noun:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="no data found")
            else:
                like=models.Like(user_id=c_user.id,noun_id=like_noun.noun_id)
                db.add(like)
                db.commit()
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="action not allowed")
    else:
        if not check.first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="action not allowed")
        else:
            if not noun:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="no data found")
            else:
                check.delete(synchronize_session=False)
                db.commit()



    return {"message":"Done"}
    #return dbm.selectUsers()