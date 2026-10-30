import os
from dotenv import load_dotenv
import psycopg

load_dotenv()

def connect():
    return psycopg.connect(
        host=os.getenv("PGHOST", "localhost"), port=os.getenv("PGPORT", "5432"),
        dbname=os.getenv("PGDATABASE", "vendas_etl"), user=os.getenv("PGUSER", "postgres"),
        password=os.getenv("PGPASSWORD", "postgres"),
    )

def ensure_schema(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            order_id TEXT PRIMARY KEY,
            order_date DATE NOT NULL,
            customer_id TEXT NOT NULL,
            product TEXT NOT NULL,
            quantity INTEGER NOT NULL CHECK (quantity > 0),
            unit_price NUMERIC(12,2) NOT NULL CHECK (unit_price > 0),
            region TEXT NOT NULL,
            loaded_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        )
        """)
    conn.commit()

def upsert_sales(conn, frame):
    sql = """INSERT INTO sales (order_id, order_date, customer_id, product, quantity, unit_price, region)
    VALUES (%s,%s,%s,%s,%s,%s,%s)
    ON CONFLICT (order_id) DO UPDATE SET order_date=EXCLUDED.order_date,
    customer_id=EXCLUDED.customer_id, product=EXCLUDED.product, quantity=EXCLUDED.quantity,
    unit_price=EXCLUDED.unit_price, region=EXCLUDED.region, loaded_at=NOW()"""
    rows = [tuple(row) for row in frame[["order_id","order_date","customer_id","product","quantity","unit_price","region"]].itertuples(index=False, name=None)]
    with conn.cursor() as cur:
        cur.executemany(sql, rows)
    conn.commit()
