"""fastMCP server exposing the store backend as MCP tools."""
from __future__ import annotations

from contextlib import contextmanager

from fastmcp import FastMCP

from app import crud, schemas
from app.database import SessionLocal


server = FastMCP("mock-store")


@contextmanager
def session_scope():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def _serialize_customers(customers):
    return [schemas.Customer.from_orm(customer).dict() for customer in customers]


def _serialize_orders(orders):
    return [schemas.Order.from_orm(order).dict() for order in orders]


def _serialize_products(products):
    return [schemas.Product.from_orm(product).dict() for product in products]


def _serialize_inventory(items):
    return [schemas.InventoryItem.from_orm(item).dict() for item in items]


@server.tool()
def list_customers() -> dict:
    """Return all customers with their metadata."""
    with session_scope() as session:
        customers = crud.list_customers(session)
        return {"customers": _serialize_customers(customers), "count": len(customers)}


@server.tool()
def list_products() -> dict:
    """Return the available products in the store."""
    with session_scope() as session:
        products = crud.list_products(session)
        return {"products": _serialize_products(products), "count": len(products)}


@server.tool()
def list_inventory() -> dict:
    """Return all inventory records."""
    with session_scope() as session:
        inventory = crud.list_inventory(session)
        return {"inventory": _serialize_inventory(inventory), "count": len(inventory)}


@server.tool()
def list_orders() -> dict:
    """Return every order with associated items and customers."""
    with session_scope() as session:
        orders = crud.list_orders(session)
        return {"orders": _serialize_orders(orders), "count": len(orders)}


@server.tool()
def get_order(order_id: int) -> dict:
    """Return a single order by ID with full detail."""
    with session_scope() as session:
        order = crud.get_order(session, order_id)
        if not order:
            return {"error": f"Order {order_id} not found"}
        return schemas.Order.from_orm(order).dict()


@server.tool()
def get_store_summary() -> dict:
    """Provide a quick overview of store metrics."""
    with session_scope() as session:
        customers = crud.list_customers(session)
        orders = crud.list_orders(session)
        inventory = crud.list_inventory(session)
        products = crud.list_products(session)

        total_inventory = sum(item.quantity for item in inventory)
        total_revenue = sum(float(order.total_amount) for order in orders)

        return {
            "metrics": {
                "customer_count": len(customers),
                "order_count": len(orders),
                "product_count": len(products),
                "inventory_units": total_inventory,
                "gross_revenue": round(total_revenue, 2),
            }
        }


def run():
    """Entrypoint used by ``python -m mcp_server``."""
    server.run()


if __name__ == "__main__":
    run()
