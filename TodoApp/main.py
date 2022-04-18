from fastapi import FastAPI, Response, status
import schemas
from api import API

# make class instacnce which have all needed function
# for a CRUD app
api = API(table_name="todo_api_xxw")


@api.app.get("/")
def hello():
    """
    Simple testing API response
    """
    return {"message": "Hello World"}


@api.app.get("/todo/{id}", status_code=status.HTTP_200_OK)
def get_item_by_uid(uid: str, response: Response):
    """
    Find item in the table by uid.
    API will response with 404 if item with given
    uid is not found in the table.
    """
    response_db, response_status = api.get_item(uid)

    if response_status == 200:
        return response_db
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return response_db


@api.app.get("/todo_all", status_code=status.HTTP_200_OK)
def get_all_items_in_list():
    """
    Return to the user all items
    in table.
    """
    return api.get_all_items()


@api.app.put("/todo/{id}", status_code=status.HTTP_200_OK)
def update_item(uid: str, task_update: str):
    """
    Update item, if item with given
    uid is not in the table then item
    will be created.
    """
    return api.update_item(uid, task_update)


@api.app.post("/create", status_code=status.HTTP_201_CREATED)
def create_item(todo_item: schemas.ToDoResponse):
    """
    Create single item. App needs task from API user
    and will generate uid for item.
    """
    return api.create_item(todo_item)


@api.app.delete("/list/{id}", status_code=status.HTTP_200_OK)
def delete_item(uid: str, response: Response):
    """
    Delete single item by its uid.
    If uid is not found in the table API will give 404 error for user
    """
    response_db, response_status = api.delete_item(uid)
    if response_status == 200:
        return response_db
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return response_db
