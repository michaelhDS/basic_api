from fastapi import FastAPI, status
from uuid import uuid4
import database
import schemas


db = database.initialize_db()
app = FastAPI()


@app.get("/")
def hello():
    return {"message": "Hello World"}


@app.get("/todo/{id}")
def get_item_by_uid(uid: str):

    table = db.Table("todo_api_xxw")
    response = table.get_item(Key={"uid": uid})

    return response


@app.get(
    "/todo/all",
)
def get_all_items_in_list():

    table = db.Table("todo_api_xxw")
    response = table.scan()

    return response


@app.put("/todo/{id}")
def update_item(uid: str, task_update: str):

    table = db.Table("todo_api_xxw")

    response = table.update_item(
        Key={
            "uid": uid
        },  # using partition key specifying which attributes will get updated
        UpdateExpression="""                
                set
                    task=:task
            """,
        ExpressionAttributeValues={  # values defined in here will get injected to update expression
            ":task": task_update
        },
        ReturnValues="UPDATED_NEW",  # return the newly updated data point
    )

    return response


@app.post("/create", status_code=status.HTTP_201_CREATED)
def create_item(todo_item: schemas.ToDoResponse):

    table = db.Table("todo_api_xxw")

    todo_item.uid = str(uuid4())
    response = table.put_item(Item=todo_item.dict())

    return response


@app.delete("/list/{id}")
def delete_item(uid: str):

    table = db.Table("todo_api_xxw")
    response = table.delete_item(Key={"uid": uid})

    return response
