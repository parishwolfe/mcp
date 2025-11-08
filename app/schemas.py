"""Pydantic schemas for API responses."""
from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import List

from pydantic import BaseModel


class InventoryItem(BaseModel):
    id: int
    product_id: int
    quantity: int
    location: str

    class Config:
        orm_mode = True


class Product(BaseModel):
    id: int
    sku: str
    name: str
    description: str
    price: Decimal

    class Config:
        orm_mode = True


class Customer(BaseModel):
    id: int
    email: str
    full_name: str
    address: str
    created_at: datetime

    class Config:
        orm_mode = True


class OrderItem(BaseModel):
    id: int
    product: Product
    quantity: int
    unit_price: Decimal

    class Config:
        orm_mode = True


class Order(BaseModel):
    id: int
    customer: Customer
    status: str
    total_amount: Decimal
    placed_at: datetime
    items: List[OrderItem]

    class Config:
        orm_mode = True
