"""Fabric notebook cell script to create a tiny synthetic source table."""

rows = [
    {"order_id": "O-1001", "customer_id": "C-001", "order_date": "2026-01-01", "amount": 120.50},
    {"order_id": "O-1002", "customer_id": "C-002", "order_date": "2026-01-02", "amount": 89.0},
    {"order_id": "O-1003", "customer_id": "C-001", "order_date": "2026-01-03", "amount": 45.25},
]

source_df = spark.createDataFrame(rows)
source_df.createOrReplaceTempView("synthetic_orders_temp")
spark.sql("CREATE SCHEMA IF NOT EXISTS source")
source_df.write.mode("overwrite").saveAsTable("source.synthetic_orders")
