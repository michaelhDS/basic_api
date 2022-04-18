from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import boto3
from boto3.resources.base import ServiceResource
import os

# Create a sqlite engine instance
engine = create_engine("sqlite:///todo.db")

# Create a DeclarativeMeta instance
Base = declarative_base()

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


class Config:
    DB_REGION_NAME = "eu-central-1"
    DB_ACCESS_KEY_ID = "AKIAYB7TY7WS7DMWNQ6R"
    DB_SECRET_ACCESS_KEY = "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"


def initialize_db() -> ServiceResource:
    ddb = boto3.resource(
        "dynamodb",
        region_name=Config.DB_REGION_NAME,
        aws_access_key_id=Config.DB_ACCESS_KEY_ID,
        aws_secret_access_key=Config.DB_SECRET_ACCESS_KEY,
    )

    return ddb
