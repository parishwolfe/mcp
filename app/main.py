"""FastAPI application exposing the mock store backend."""
from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException
from fastmcp.integrations.fastapi import mount_mcp_server

from . import crud, schemas
from .database import get_session
from mcp_server.server import server as mcp_server


app = FastAPI(title="MCP Mock Store API", version="1.0.0")

# Mount the fastMCP server following the documented FastAPI integration pattern.
mount_mcp_server(app, mcp_server, path="/mcp")


@app.get("/customers", response_model=list[schemas.Customer])
def get_customers(session=Depends(get_session)):
    return crud.list_customers(session)


@app.get("/customers/{customer_id}", response_model=schemas.Customer)
def get_customer(customer_id: int, session=Depends(get_session)):
    customer = crud.get_customer(session, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@app.get("/products", response_model=list[schemas.Product])
def get_products(session=Depends(get_session)):
    return crud.list_products(session)


@app.get("/inventory", response_model=list[schemas.InventoryItem])
def get_inventory(session=Depends(get_session)):
    return crud.list_inventory(session)


@app.get("/orders", response_model=list[schemas.Order])
def get_orders(session=Depends(get_session)):
    return crud.list_orders(session)


@app.get("/orders/{order_id}", response_model=schemas.Order)
def get_order(order_id: int, session=Depends(get_session)):
    order = crud.get_order(session, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
