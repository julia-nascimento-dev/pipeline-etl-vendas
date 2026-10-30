CREATE TABLE IF NOT EXISTS sales (
  order_id TEXT PRIMARY KEY, order_date DATE NOT NULL, customer_id TEXT NOT NULL,
  product TEXT NOT NULL, quantity INTEGER NOT NULL CHECK (quantity > 0),
  unit_price NUMERIC(12,2) NOT NULL CHECK (unit_price > 0), region TEXT NOT NULL,
  loaded_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
