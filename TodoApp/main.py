from email import message
import imp
from typing import List
from urllib import response
from fastapi import FastAPI, status, HTTPException
from sqlalchemy import engine
import database
from sqlalchemy.orm import Session
from database import Base, engine
import models
import schemas


# Create the database
Base.metadata.create_all(engine)

app = FastAPI()


@app.get("/list/{id}")  # response_model=schemas.ToDoResponse
def get_item_by_id(id: int):

    session = Session(bind=engine, expire_on_commit=False)

    todo_item = session.query(models.ToDoItems).get(id)

    session.close()

    if todo_item:
        return todo_item
    else:
        raise HTTPException(
            status_code=404, detail=f"Todo item {id} not found in a list"
        )


@app.get("/list", response_model=List[schemas.ToDoResponse])
def get_all_items_in_list():

    session = Session(bind=engine, expire_on_commit=False)

    todo_items_list = session.query(models.ToDoItems).all()
    # print(todo_items_list)
    session.close()
    return todo_items_list


@app.post(
    "/list", status_code=status.HTTP_201_CREATED
)  # response_model=schemas.ToDoTask,
def create_item(todo_item: schemas.ToDoTask):

    session = Session(bind=engine, expire_on_commit=False)

    todo_db = models.ToDoItems(task=todo_item.task, owner_id="user1")

    session.add(todo_db)
    session.commit()

    # add it to the session and commit it
    session.add(todo_db)
    session.commit()
    session.refresh(todo_db)

    # close the session
    session.close()

    return todo_db


@app.put("/list/{id}")
def update_item(id: int, task: str):
    session = Session(bind=engine, expire_on_commit=False)

    todo_item = session.query(models.ToDoItems).get(id)

    if todo_item:
        todo_item.task = task
        session.commit()
        session.close()
        return {"item_id": id, "status": f"succesfuly change to: '{task}'"}

    else:
        session.close()
        raise HTTPException(status_code=404, detail=f"Item id {id} not found")


@app.delete("/list/{id}")
def delete_item(id: int):

    session = Session(bind=engine, expire_on_commit=False)
    todo_item = session.query(models.ToDoItems).get(id)

    if todo_item:
        session.delete(todo_item)
        session.commit()
        session.close()
        return {"response": f"Item id {id} was succesfully deleted"}

    else:
        raise HTTPException(status_code=404, detail=f"Todo item {id} not found")
