from fastapi import HTTPException, status,Depends,Response,APIRouter
from numpy import not_equal
from . import schema,utils
from sqlalchemy.orm import Session
from DB.SqlAlchemy import get_db
from DB import models
from typing import List
from sqlalchemy.exc import IntegrityError
import pandas as pd
import string
import re

router=APIRouter(
    prefix="/load",
    tags=["load"]
)
@router.get("/")
def load(db: Session = Depends(get_db)):
    """
    df=pd.read_csv("app\Dataout.csv")

    df["German_Noun"]=df.German_Noun.str.replace(r'[0-9]', '')
    df["German_Noun"]=df.German_Noun.str.replace(r'[\']', '')
    df["German_Noun"]=df.German_Noun.str.strip()

    df["English_Description"]=df.English_Description.str.replace(r'[0-9]', '')
    df["English_Description"]=df.English_Description.str.replace(r'[\']', '')
    df["English_Description"]=df.English_Description.str.strip()

    df["Gender"]=df.Gender.str.replace(r'f', 'Die')
    df["Gender"]=df.Gender.str.replace(r'm', 'Der')
    df["Gender"]=df.Gender.str.replace(r'n', 'Das')

    #t2=teststr.translate(str.maketrans('', '', string.punctuation)).translate(str.maketrans('', '', string.digits))
    df.dropna(inplace=True)
    print(df.iloc[5:50])
    for i in range(len(df)):
        noun=df.iloc[i]["German_Noun"]
        eng=df.iloc[i]["English_Description"]
        

        print(noun,"   ",eng)
        existing_record=db.query(models.Noun).filter(models.Noun.noun==noun).first()
        neweng=models.EngDef(definition=eng,noun_id=existing_record.id)
        eg_record=db.query(models.EngDef).filter(models.EngDef.definition==eng).first()

        if not eg_record:
            db.add(neweng)
            db.commit()
        elif eg_record.noun_id != existing_record.id:
            db.add(neweng)
            db.commit()"""


    return{"data":"done"}