from fastapi import APIRouter, Response, status
from config.db import conn
from schemas.user import userEntity, usersEntity
from models.user import User
from passlib.hash import sha256_crypt
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT

user = APIRouter()

@user.get('/users', response_model=list[User], tags=["users"])
def find_all_user():
  return usersEntity(conn.local.user.find())

@user.post('/users', response_model=User, tags=["users"])
def create_user(user: User):
  new_user = dict(user)
  new_user["password"] = sha256_crypt.encrypt(new_user["password"])

  objectId = conn.local.user.insert_one(new_user).inserted_id
  user = conn.local.user.find_one({"_id": objectId})
  print(user)

  return userEntity(user)

@user.get('/users/{id}', response_model=User, tags=["users"])
def find_user(id: str):
  return userEntity(conn.local.user.find_one({"_id": ObjectId(id)}))

@user.put('/users/{id}', response_model=User, tags=["users"])
def update_user(id: str, user: User):
    new_user = dict(user)
    new_user["password"] = sha256_crypt.encrypt(new_user["password"])

    conn.local.user.find_one_and_update({"_id": ObjectId(id)}, {"$set": new_user})
    return userEntity(conn.local.user.find_one({"_id": ObjectId(id)}))

@user.delete('/users/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def delete_user(id: str):
  conn.local.user.find_one_and_delete({"_id": ObjectId(id)})
  return Response(status_code=HTTP_204_NO_CONTENT)