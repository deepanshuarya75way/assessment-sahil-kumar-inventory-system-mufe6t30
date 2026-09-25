CREATE TABLE IF NOT EXISTS  forecasts(
  id SERIAL PRIMARY KEY,
  product_id  UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  daily_demand  FLOAT NOT NULL,
  stockout_date DATE,
  reorder_quantity INTEGER NOT NULL,
  confidence VARCHAR(20) NOT NULL,
  history_start DATE NOT NULL,
  history_end DATE NOT NULL,
  create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);