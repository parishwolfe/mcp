"""Database access helpers for the store backend."""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from . import models


def list_customers(session: Session):
    return session.scalars(select(models.Customer)).all()


def get_customer(session: Session, customer_id: int):
    return session.get(models.Customer, customer_id)


def list_products(session: Session):
    return session.scalars(select(models.Product)).all()


def list_inventory(session: Session):
    return session.scalars(select(models.InventoryItem)).all()


def list_orders(session: Session):
    stmt = select(models.Order).options(
        selectinload(models.Order.customer),
        selectinload(models.Order.items).selectinload(models.OrderItem.product),
    )
    return session.scalars(stmt).unique().all()


def get_order(session: Session, order_id: int):
    return session.get(models.Order, order_id)
