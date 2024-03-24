from sqlmodel import Field, Relationship, SQLModel
from typing import Literal
from enum import Enum

# Shared properties
# TODO replace email str with EmailStr when sqlmodel supports it
class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str


# TODO replace email str with EmailStr when sqlmodel supports it
class UserCreateOpen(SQLModel):
    email: str
    password: str
    full_name: str | None = None


# Properties to receive via API on update, all are optional
# TODO replace email str with EmailStr when sqlmodel supports it
class UserUpdate(UserBase):
    email: str | None = None  # type: ignore
    password: str | None = None


# TODO replace email str with EmailStr when sqlmodel supports it
class UserUpdateMe(SQLModel):
    full_name: str | None = None
    email: str | None = None


class UpdatePassword(SQLModel):
    current_password: str
    new_password: str


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner")
    transactions: list["TransactionBase"] = Relationship(back_populates="owner")
    budgets: list["BudgetBase"] = Relationship(back_populates="owner")
    categories: list["Category"] = Relationship(back_populates="owner")


# Properties to return via API, id is always required
class UserOut(UserBase):
    id: int


class UsersOut(SQLModel):
    data: list[UserOut]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str
    description: str | None = None


# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = None  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemOut(ItemBase):
    id: int
    owner_id: int


class ItemsOut(SQLModel):
    data: list[ItemOut]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: int | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str


class Priority(SQLModel, table=True):
    id: int = Field(primary_key = True)
    description: str
    transactions: list["TransactionBase"] = Relationship(back_populates="priority")

class TransactionType(SQLModel, table=True):
    id: int = Field(primary_key = True)
    description: str
    transactions: list["TransactionBase"] = Relationship(back_populates="transaction_type")

class ExpenseType(SQLModel, table=True):
    id: int = Field(primary_key = True)
    description: str
    categories: list["Category"] = Relationship(back_populates="expense_type")

class Category(SQLModel, table=True):
    id: int = Field(primary_key = True)
    user_id: int = Field(foreign_key = "user.id")
    description: str
    expense_type_id: int = Field(foreign_key = "expense_type.id")
    transactions: list["TransactionBase"] = Relationship(back_populates="category")

class TransactionBase(SQLModel, table=True):
    id: int = Field(primary_key = True)
    user_id = int = Field(foreign_key = "user.id")
    amount: float
    description: str
    priority_id: int = Field(foreign_key = "priority.id")
    transaction_type_id: int = Field(foreign_key = "transaction_type.id")
    category_id: int = Field(foreign_key = "category.id")

class BudgetBase(SQLModel, table=True):
    id: int = Field(primary_key = True)
    user_id = int = Field(foreign_key = "user.id")
    amount: float
    expenses: float
    category_id: int = Field(foreign_key = "category.id")
