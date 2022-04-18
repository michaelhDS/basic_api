from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import boto3
from boto3.resources.base import ServiceResource
import os
import pathlib
from dotenv import load_dotenv

# Create a sqlite engine instance
engine = create_engine("sqlite:///todo.db")

# Create a DeclarativeMeta instance
Base = declarative_base()

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


base_dir = pathlib.Path(__file__).parent
load_dotenv(base_dir.joinpath(".env"))


class Config:
    DB_REGION_NAME = os.getenv("DB_REGION_NAME")
    DB_ACCESS_KEY_ID = os.getenv("DB_ACCESS_KEY_ID")
    DB_SECRET_ACCESS_KEY = os.getenv("DB_SECRET_ACCESS_KEY")


def initialize_db() -> ServiceResource:
    ddb = boto3.resource(
        "dynamodb",
        region_name=Config.DB_REGION_NAME,
        aws_access_key_id=Config.DB_ACCESS_KEY_ID,
        aws_secret_access_key=Config.DB_SECRET_ACCESS_KEY,
    )

    return ddb
