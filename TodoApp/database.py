import boto3
from boto3.resources.base import ServiceResource
import os
import pathlib
from dotenv import load_dotenv


class Database:
    """
    Basic class to manage database.
    """

    def __init__(self) -> None:
        self.load_env()
        self.DB_REGION_NAME = os.getenv("DB_REGION_NAME")
        self.DB_ACCESS_KEY_ID = os.getenv("DB_ACCESS_KEY_ID")
        self.DB_SECRET_ACCESS_KEY = os.getenv("DB_SECRET_ACCESS_KEY")

    def load_env(self):
        """
        Load .env config file
        """
        base_dir = pathlib.Path(__file__).parent
        load_dotenv(base_dir.joinpath(".env"))

    def initialize_db(self) -> ServiceResource:
        """
        Initialize database with
        boto3 library.
        """
        ddb = boto3.resource(
            "dynamodb",
            region_name=self.DB_REGION_NAME,
            aws_access_key_id=self.DB_ACCESS_KEY_ID,
            aws_secret_access_key=self.DB_SECRET_ACCESS_KEY,
        )

        return ddb
