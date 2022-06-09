
import imp
from fastapi import FastAPI

from DB import models
from DB.SqlAlchemy import engine,get_db
from .config import settings
from .routers.user import router as user_router
from .routers.auth import router as auth_router
from .routers.word import router as noun_router
from .routers.like import router as like_router
from .FirstTimeDataloader import router as FT
from .FirstTimeDataloader import load

models.Base.metadata.create_all(bind=engine)



app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(noun_router)
app.include_router(like_router)
app.include_router(FT)
@app.get("/")
def root():
    return {"message": "Hello World"}

"""while True:
    dbm=DBM.DbManager(host=host,dbName=database,password=password,user=user)
    if dbm.connected:
        print("DB Connected")
        break

    time.sleep(3)"""