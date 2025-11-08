# MCP Mock Store Example

This repository contains an end-to-end example of a [fastMCP](https://github.com/josStorer/fastmcp) server that exposes a mock e-commerce store backed by a FastAPI application and a PostgreSQL database. It demonstrates how to share the same data source between a REST API and Model Context Protocol (MCP) tools so that conversational AI agents can explore store information such as customers, inventory, and orders.

## Project layout

```
.
├── app/                  # FastAPI application (SQLAlchemy models, schemas, CRUD helpers)
├── mcp_server/           # fastMCP server exposing store data as tools
├── sql/                  # SQL scripts for schema and seed data
├── docker-compose.yml    # Local PostgreSQL instance with preloaded data
├── requirements.txt      # Python dependencies for both servers
└── .env.example          # Example environment variables
```

## Prerequisites

* Python 3.11+
* [Docker](https://www.docker.com/) and Docker Compose (v2 or newer)
* `pip` for installing Python dependencies

## 1. Start the database

```bash
docker compose up -d
```

The PostgreSQL container mounts the `sql/` directory into `/docker-entrypoint-initdb.d`, so the schema (`create_tables.sql`) and sample data (`seed_data.sql`) are loaded automatically the first time the container starts.

## 2. Configure environment variables

Copy the example environment file and adjust it if you changed any credentials or hostnames:

```bash
cp .env.example .env
```

Both the FastAPI service and the fastMCP server read the `DATABASE_URL` environment variable. The default connection string assumes you are running locally with the `docker-compose.yml` configuration.

## 3. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 4. Run the FastAPI backend

```bash
uvicorn app.main:app --reload
```

### Example endpoints

* `GET /customers` – list all customers
* `GET /customers/{id}` – retrieve a single customer
* `GET /products` – browse available products
* `GET /inventory` – inspect inventory levels
* `GET /orders` – view orders including nested line items
* `GET /orders/{id}` – fetch a specific order

## 5. Run the fastMCP server

```bash
python -m mcp_server
```

The server registers the following tools:

| Tool name          | Description |
| ------------------ | ----------- |
| `list_customers`   | Returns all customers and their metadata. |
| `list_products`    | Lists available products. |
| `list_inventory`   | Provides current inventory levels. |
| `list_orders`      | Retrieves orders with customer and line item data. |
| `get_order`        | Returns a single order by ID, or an error if missing. |
| `get_store_summary`| Aggregates counts and high-level metrics. |

Each tool responds with JSON derived from the same SQLAlchemy models used by the FastAPI backend, ensuring consistent representations across HTTP and MCP interfaces.

## 6. Connect from popular AI chatbots

Below are quick-start notes for common MCP-compatible clients. Substitute the path to your virtual environment's Python interpreter if different (e.g., `.venv/bin/python`).

### Anthropic Claude Desktop

1. Open **Claude Desktop** and navigate to **Settings → Configure MCP Servers**.
2. Add a new server with:
   * **Command**: `python`
   * **Arguments**: `-m mcp_server`
   * **Working directory**: the root of this repository.
3. Ensure the `DATABASE_URL` environment variable is available to Claude (e.g., by launching Claude from a shell session where it is exported).
4. Claude can now call tools such as `get_store_summary` during conversations.

### Cursor IDE

1. Open Cursor and run the command **Cursor: Configure MCP Servers**.
2. Create an entry with the command `python` and arguments `-m mcp_server`.
3. Optionally specify environment variables via the configuration panel so the MCP server can reach the PostgreSQL instance.
4. Use the “Connect MCP Server” command to make tools available in the chat sidebar.

### VS Code + Continue

1. Install the [Continue](https://www.continue.dev/) extension (version 0.9.0+).
2. Open the Continue settings (`continue.json`) and add:

   ```json
   {
     "servers": [
       {
         "name": "mock-store",
         "command": "python",
         "args": ["-m", "mcp_server"],
         "cwd": "${workspaceFolder}",
         "env": {
           "DATABASE_URL": "postgresql+psycopg2://mcp_user:mcp_password@localhost:5432/mcp_store"
         }
       }
     ]
   }
   ```

3. Restart Continue; the mock store tools will appear in the MCP tool palette.

### OpenAI Desktop / ChatGPT Desktop (beta MCP support)

1. Launch the client from a terminal with the virtual environment activated so the MCP server dependencies are available.
2. In the MCP configuration UI, add a custom server pointing to `python -m mcp_server`.
3. Use the UI to map environment variables or rely on your shell environment.

> **Tip:** If a client requires an absolute path to the interpreter, run `which python` (Linux/macOS) or `where python` (Windows) inside the virtual environment and paste that path into the MCP configuration.

## Database management

* **Reset data:** stop the containers (`docker compose down`), delete the volume (`docker volume rm mcp_postgres-data`), and start again.
* **Manual migrations:** you can rerun the SQL scripts with `psql`:

  ```bash
  psql postgresql://mcp_user:mcp_password@localhost:5432/mcp_store -f sql/create_tables.sql
  psql postgresql://mcp_user:mcp_password@localhost:5432/mcp_store -f sql/seed_data.sql
  ```

## Testing the MCP tools manually

Once the server is running, you can issue direct requests with the `fastmcp` client utilities:

```bash
python -m fastmcp.client --command "get_store_summary"
```

Refer to the `fastmcp` documentation for more advanced usage such as streaming outputs or structured arguments.

## License

This example is provided under the MIT license. Use it as a starting point for your own MCP-integrated services.
