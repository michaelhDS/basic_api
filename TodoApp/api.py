from genericpath import exists
from fastapi import FastAPI, status, Response
from uuid import uuid4
import schemas
from database import Database


class API:
    """
    Basic class to maange API,
    its functions and configuration.
    """

    def __init__(self, table_name) -> None:
        self.app = FastAPI()
        self.database = Database()
        self.db = self.database.initialize_db()
        self.table_name = table_name
        self.table = self.db.Table(self.table_name)

    def get_item(self, uid: str):
        """
        Find single item
        """
        response = self.table.get_item(Key={"uid": uid})

        if response.get("Item"):
            status = 200
        else:
            status = 404
            response = {"message": "item not found"}

        return response, status

    def get_all_items(self):
        """
        Return all items inside the table
        """
        response = self.table.scan()

        return response

    def update_item(self, uid: str, task_update: str):
        """
        Try to update single item
        """
        response = self.table.update_item(
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

    def create_item(self, todo_item: schemas.ToDoResponse):
        """
        Create single item
        """
        todo_item.uid = str(uuid4())
        response = self.table.put_item(Item=todo_item.dict())
        return response

    def delete_item(self, uid: str):
        """
        Delete single items
        """
        try:
            response = self.table.delete_item(
                Key={"uid": uid}, ConditionExpression="attribute_exists (uid)"
            )
            status = 200
            return response, status

        except:
            response = {"message": "item does not exist"}
            status = 404
            return response, status
