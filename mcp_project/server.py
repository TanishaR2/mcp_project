from mcp.server.fastmcp import FastMCP
import psycopg2
import os

# --- Setup MCP server ---
mcp = FastMCP(name="PostgresQnA")

# --- Database connection details (from env vars, not hardcoded) ---
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "dbname": os.getenv("DB_NAME", "datadesign_local"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres")
}

def run_sql(query: str):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute(query)
        # Handle SELECT vs non-SELECT
        if cur.description:
            rows = cur.fetchall()
        else:
            conn.commit()
            rows = f"{cur.rowcount} rows affected"
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def query_database(query: str) -> str:
    """
    Run a SQL query on the Postgres database and return results.
    Example:
      query_database("SELECT * FROM mytable LIMIT 5;")
    """
    result = run_sql(query)
    return str(result)

if __name__ == "__main__":
    print("Starting MCP server...")
    mcp.run()
