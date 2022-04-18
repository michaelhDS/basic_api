from email import message
import imp
from typing import List
from urllib import response
from fastapi import FastAPI, status, HTTPException
from sqlalchemy import engine
import database
from sqlalchemy.orm import Session
from database import Base, engine
import schemas
from uuid import uuid4


# Create the database
Base.metadata.create_all(engine)

db = database.initialize_db()

app = FastAPI()


@app.get("/list/{id}")  # response_model=schemas.ToDoResponse
def get_item_by_id(uid: str):

    table = db.Table("todo_api_xxw")
    response = table.get_item(Key={"uid": uid})

    return response


@app.get(
    "/list",
)  # response_model=List[schemas.ToDoResponse]
def get_all_items_in_list():

    table = db.Table("todo_api_xxw")
    response = table.scan()

    return response


@app.put("/list/{id}")
def update_item(uid: str, task: str):

    table = db.Table("todo_api_xxw")

    response = table.update_item(  # update single item
        Key={
            "uid": uid
        },  # using partition key specifying which attributes will get updated
        UpdateExpression="""                
                set
                    task=:task
            """,
        ExpressionAttributeValues={  # values defined in here will get injected to update expression
            ":task": task
        },
        ReturnValues="UPDATED_NEW",  # return the newly updated data point
    )

    return response


@app.post(
    "/create", status_code=status.HTTP_201_CREATED
)  # response_model=schemas.ToDoTask,
def create_item2x(todo_item: schemas.ToDoResponse):

    table = db.Table("todo_api_xxw")

    todo_item.uid = str(uuid4())
    response = table.put_item(Item=todo_item.dict())

    return response


@app.delete("/list/{id}")
def delete_item(uid: str):

    table = db.Table("todo_api_xxw")
    response = table.delete_item(Key={"uid": uid})

    return response
