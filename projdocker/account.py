# THINGS TO DO:
# determine if want to add edit profile functionality
# determine if want to call error microservice or not for errors
import jwt
import bcrypt
import uvicorn
import graphene
import sqlalchemy
from os import environ
from fastapi import FastAPI
from datetime import datetime
from google.oauth2 import id_token
from google.auth.transport import requests
from starlette_graphene3 import GraphQLApp
from fastapi.middleware.cors import CORSMiddleware

engine = sqlalchemy.create_engine(environ.get('dbURL'), echo=True)

account_table = sqlalchemy.Table(
    "account",
    sqlalchemy.MetaData(),
    sqlalchemy.Column("fullname", sqlalchemy.String(64)),
    sqlalchemy.Column("passwd", sqlalchemy.String(64)),
    sqlalchemy.Column("email", sqlalchemy.String(64))
)

follower_table = sqlalchemy.Table(
    "follower",
    sqlalchemy.MetaData(),
    sqlalchemy.Column("email", sqlalchemy.String(64)),
    sqlalchemy.Column("followemail", sqlalchemy.String(64))
)

class Followers(graphene.ObjectType):
    followfullname = graphene.String()
    followemail = graphene.String()

class User(graphene.ObjectType):
    fullname = graphene.String()
    email = graphene.String()
    followers = graphene.List(Followers)

    def resolve_followers(parent, info):
        emails = []
        followerlist = []
        fstmt = sqlalchemy.select(follower_table.c.followemail).where(follower_table.c.email == parent.email)
        with engine.connect() as conn:
            for row in conn.execute(fstmt):
                emails.append(row[0])
        for f_email in emails:
            fstmt2 = sqlalchemy.select(account_table.c.fullname).where(account_table.c.email == f_email)
            with engine.connect() as conn:
                fname = conn.execute(fstmt2).first()
                followerlist.append(Followers(followfullname=fname[0], followemail=f_email))
        return followerlist

class Query(graphene.ObjectType):
    user = graphene.Field(User, em=graphene.String(required=True))

    def resolve_user(root, info, em):
        mystmt = sqlalchemy.select(account_table.c.fullname, account_table.c.email).where(account_table.c.email == em)
        result = None
        with engine.connect() as conn:
            result = conn.execute(mystmt).first()
        return User(fullname=result[0], email=result[1])

class AddFollower(graphene.Mutation):
    class Arguments:
        useremail = graphene.String()
        f_email = graphene.String()

    status = graphene.Boolean()

    def mutate(root, info, useremail, f_email):
        stmt = sqlalchemy.insert(follower_table).values(email=useremail, followemail=f_email)
        compiled = stmt.compile()
        with engine.connect() as conn:
            result = conn.execute(stmt)
        return AddFollower(status=True)

class DelFollower(graphene.Mutation):
    class Arguments:
        useremail = graphene.String()
        f_email = graphene.String()

    status = graphene.Boolean()

    def mutate(root, info, useremail, f_email):
        stmt = sqlalchemy.delete(follower_table).where((follower_table.c.email == useremail) & (follower_table.c.followemail == f_email))
        with engine.connect() as conn:
            result = conn.execute(stmt)
        return DelFollower(status=True)

class CreateAccount(graphene.Mutation):
    class Arguments:
        fullname = graphene.String()
        passwd = graphene.String()
        email = graphene.String()

    status = graphene.Boolean()
    token = graphene.ID()
    message = graphene.String()

    def mutate(root, info, fullname, passwd, email):
        newtoken = None
        message = ""
        if len(fullname) > 64 or len(passwd) > 64 or len(email) > 64:
            message = "User credentials exceed allowable length"
            return CreateAccount(status=False, token=newtoken, message=message)
        check_stmt = sqlalchemy.select(account_table).where(account_table.c.email == email)
        check_row = None
        with engine.connect() as conn:
            for row in conn.execute(check_stmt):
                check_row = row
        if check_row != None:
            message = "The provided email is already associated with an existing account"
            return CreateAccount(status=False, token=newtoken, message=message)
        token_payload = {"sub": email, "name": fullname}
        token_secret = "esd_is_so_fun_omg123"
        newtoken = jwt.encode(payload=token_payload, key=token_secret)
        hashed_pw = bcrypt.hashpw(passwd.encode('utf-8'), bcrypt.gensalt())
        stmt = sqlalchemy.insert(account_table).values(fullname=fullname, passwd=hashed_pw, email=email)
        compiled = stmt.compile()
        with engine.connect() as conn2:
            result = conn2.execute(stmt)
        return CreateAccount(status=True, token=newtoken, message=message)

class NormalSignin(graphene.Mutation):
    class Arguments:
        email = graphene.String()
        passwd = graphene.String()

    status = graphene.Boolean()
    token = graphene.ID()
    message = graphene.String()

    def mutate(root, info, email, passwd):
        user = None
        message = ""
        stmt = sqlalchemy.select(account_table.c.passwd, account_table.c.email, account_table.c.fullname).where(account_table.c.email == email)
        with engine.connect() as conn:
            for row in conn.execute(stmt):
                user = row
        if user != None:
            if bcrypt.checkpw(passwd.encode("utf-8"), user[0].encode("utf-8")):
                token_payload = {"sub": user[1], "name": user[2]}
                token_secret = "esd_is_so_fun_omg123"
                return_token = jwt.encode(payload=token_payload, key=token_secret)
                return NormalSignin(status=True, token=return_token, message=message)
            else:
                # determine if need call error microservice or handle error here
                # Error wrong password
                message = "Incorrect email or password"
                return NormalSignin(status=False, token=None, message=message)
        else:
            # determine if need call error microservice or handle error here
            # Error no user found based on given email
            message = "Incorrect email or password"
            return NormalSignin(status=False, token=None, message=message)

class GoogleSignin(graphene.Mutation):
    class Arguments:
        gtoken = graphene.String()

    status = graphene.Boolean()
    token = graphene.ID()
    message = graphene.String()

    def mutate(root, info, gtoken):
        message = ""
        try:
            idinfo = id_token.verify_oauth2_token(gtoken, requests.Request(), "1098783399063-n68jhe1kmf1vhjonp5mjp0im0d5n1oha.apps.googleusercontent.com")
            userid = idinfo["sub"]
            name = idinfo['name']
            email = idinfo['email']
            token_payload = {"sub": email, "name": name}
            token_secret = "esd_is_so_fun_omg123"
            return_token = jwt.encode(payload=token_payload, key=token_secret, algorithm="HS256")
            user = None
            stmt = sqlalchemy.select(account_table.c.email).where(account_table.c.email == email)
            with engine.connect() as conn:
                for row in conn.execute(stmt):
                    user = row
            if user != None: # scenario where user has an existing account
                return GoogleSignin(status=True, token=return_token, message=message)
            else: # scenario where user is a new user (no existing account)
                if len(name) > 32:
                    message = "User credentials exceed allowable length"
                    return GoogleSignin(status=False, token=return_token, message=message)
                else:
                    stmt = sqlalchemy.insert(account_table).values(fullname=name, passwd=None, email=idinfo["email"])
                    compiled = stmt.compile()
                    with engine.connect() as conn2:
                        result = conn2.execute(stmt)
                    return GoogleSignin(status=True, token=return_token, message=message)
        except ValueError:
            return GoogleSignin(status=False, token=None, message="Your Google token is invalid")

class Mutations(graphene.ObjectType):
    create_account = CreateAccount.Field()
    normal_signin = NormalSignin.Field()
    google_signin = GoogleSignin.Field()
    add_follower = AddFollower.Field()
    del_follower = DelFollower.Field()

app = FastAPI()
origins = ["http://localhost"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.add_route("/graphql", GraphQLApp(schema=graphene.Schema(query=Query, mutation=Mutations)))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
