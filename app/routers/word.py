from fastapi import HTTPException, status,Depends,Response,APIRouter
from .. import schema,utils,oauth2
from sqlalchemy.orm import Session
from DB.SqlAlchemy import get_db
from DB import models
from typing import List
from sqlalchemy.exc import IntegrityError
import random

router=APIRouter(
    prefix="/words",
    tags=["Words"]
)


@router.get("/",response_model=list[schema.Defination])
def get_word(db: Session = Depends(get_db),c_user=Depends(oauth2.get_current_user),limit=1):
    ren_num=random.randint(0,483284)
    word=db.query(models.EngDef).filter(models.EngDef.noun_id>=ren_num,models.EngDef.noun_id<=ren_num+int(limit)).all()
    if not word:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str("Please try again"))
    return word #dbm.selectUserById(id)