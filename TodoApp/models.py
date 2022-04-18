import email
import string
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hash_password = Column(String)
    todos = relationship("ToDoItems", back_populates="owner")


class ToDoItems(Base):
    __tablename__ = "todo_items_list"
    id = Column(Integer, primary_key=True)
    task = Column(String(256))
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("Users", back_populates="todos")
