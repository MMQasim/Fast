from email import message
import psycopg2
from psycopg2.extras import RealDictCursor

#host="" ,database="",password="",user="",cursor_factory=RealDictCursor

class DbManager():

    def __init__(self,host,dbName,password,user):
        self.host=host
        self.dbName=dbName
        self.password=password
        self.user=user
        try:
            self.conn= psycopg2.connect(host=self.host ,database=self.dbName,password=self.password,user=self.user,cursor_factory=RealDictCursor)
            self.conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            self.cur = self.conn.cursor()
            
            
            self.connected=True
        except psycopg2.Error as error:
            raise ValueError(f"UNABLE TO CONNECT TO DATABASE\n{error}")



    def selectUsers(self):
        table="Users"
        self.cur.execute("""SELECT * FROM "Users";""")
        return self.cur.fetchall()

    def selectUserById(self,id):
        table="Users"
        try:
            self.cur.execute("""SELECT * FROM "Users" WHERE "id"=%s;""",(str(id),))
            temp=self.cur.fetchall()
            if len(temp)==0:
                raise ValueError("Data not found")
            return temp
        except Exception as err:
            print(err)
            raise ValueError("Data not found")

    def createUser(self,user):
        try:
            self.cur.execute("""INSERT INTO "Users" ("firstName", "lastName", "email", "phoneNumber", "password") VALUES (%s, %s, %s, %s, %s) RETURNING *;""",
            (user.firstName,user.lastName,user.email,user.phoneNumber,user.password))
            temp=self.cur.fetchone()
            self.conn.commit()
            return temp
        except Exception as err:
            raise ValueError("User Already exist")
        print(user.firstName)


