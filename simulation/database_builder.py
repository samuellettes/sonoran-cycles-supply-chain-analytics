"""
database_builder.py

Builds a SQLite database from the Sonoran Cycles simulation CSV outputs.

Responsibilities:
- Load master data tables
- Load raw simulation output tables
- Load analytics summary tables
- Create helpful SQL indexes
- Validate table row counts
"""

from pathlib import Path
import sqlite3

import pandas as pd


MASTER_TABLES = {
    "products": "data/products.csv",
    "customers": "data/customers.csv",
    "suppliers": "data/suppliers.csv",
    "calendar": "data/calendar.csv",
}


OUTPUT_TABLES = {
    "sales_orders": "outputs/sales_orders.csv",
    "sales_order_lines": "outputs/sales_order_lines.csv",
    "purchase_orders": "outputs/purchase_orders.csv",
    "inventory_history": "outputs/inventory_history.csv",
    "forecast_history": "outputs/forecast_history.csv",
    "daily_order_summary": "outputs/daily_order_summary.csv",
}


ANALYTICS_TABLES = {
    "monthly_sales_summary": "outputs/analytics/monthly_sales_summary.csv",
    "model_performance_summary": "outputs/analytics/model_performance_summary.csv",
    "inventory_kpi_summary": "outputs/analytics/inventory_kpi_summary.csv",
    "forecast_accuracy_by_model": "outputs/analytics/forecast_accuracy_by_model.csv",
    "supplier_performance_summary": "outputs/analytics/supplier_performance_summary.csv",
    "daily_kpi_summary": "outputs/analytics/daily_kpi_summary.csv",
}


def get_project_root():
    """
    Returns the project root directory.
    """

    return Path(__file__).resolve().parent.parent


def clean_column_names(df):
    """
    Cleans column names for SQLite compatibility.
    """

    df = df.copy()

    df.columns = [
        column.strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
        for column in df.columns
    ]

    return df


def load_csv_to_table(conn, project_root, table_name, relative_csv_path):
    """
    Loads one CSV file into a SQLite table.
    """

    csv_path = project_root / relative_csv_path

    if not csv_path.exists():
        raise FileNotFoundError(f"Missing CSV file: {csv_path}")

    df = pd.read_csv(csv_path)
    df = clean_column_names(df)

    df.to_sql(
        table_name,
        conn,
        if_exists="replace",
        index=False,
    )

    return len(df)


def create_indexes(conn):
    """
    Creates indexes to make common joins and filters faster.
    """

    index_statements = [
        """
        CREATE INDEX IF NOT EXISTS idx_products_product_id
        ON products(product_id);
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_customers_customer_id
        ON customers(customer_id);
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_suppliers_supplier_id
        ON suppliers(supplier_id);
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_calendar_date
        ON calendar(date);
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_sales_orders_sales_order_id
        ON sales_orders(sales_order_id);
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_sales_orders_order_date
        ON sales_orders(order_date);
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_sales_orders_customer_id
        ON sales_orders(customer_id);
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_sales_order_lines_sales_order_id
        ON sales_order_lines(sales_order_id);
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_sales_order_lines_product_id
        ON sales_order_lines(product_id);
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_purchase_orders_product_id
        ON purchase_orders(product_id);
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_purchase_orders_supplier_id
        ON purchase_orders(supplier_id);
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_inventory_history_product_id
        ON inventory_history(product_id);
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_inventory_history_snapshot_date
        ON inventory_history(snapshot_date);
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_forecast_history_product_id
        ON forecast_history(product_id);
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_forecast_history_forecast_month
        ON forecast_history(forecast_month);
        """,
    ]

    for statement in index_statements:
        conn.execute(statement)

    conn.commit()


def get_table_counts(conn):
    """
    Returns row counts for all tables in the database.
    """

    tables = pd.read_sql_query(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name;
        """,
        conn,
    )

    counts = []

    for table_name in tables["name"]:
        row_count = pd.read_sql_query(
            f"SELECT COUNT(*) AS row_count FROM {table_name};",
            conn,
        )["row_count"].iloc[0]

        counts.append(
            {
                "table_name": table_name,
                "row_count": int(row_count),
            }
        )

    return pd.DataFrame(counts)


def build_sqlite_database(database_name="sonoran_cycles.db"):
    """
    Builds the full SQLite database from CSV files.
    """

    project_root = get_project_root()

    database_folder = project_root / "database"
    database_folder.mkdir(exist_ok=True)

    database_path = database_folder / database_name

    all_tables = {}
    all_tables.update(MASTER_TABLES)
    all_tables.update(OUTPUT_TABLES)
    all_tables.update(ANALYTICS_TABLES)

    with sqlite3.connect(database_path) as conn:
        load_results = []

        for table_name, relative_csv_path in all_tables.items():
            row_count = load_csv_to_table(
                conn=conn,
                project_root=project_root,
                table_name=table_name,
                relative_csv_path=relative_csv_path,
            )

            load_results.append(
                {
                    "table_name": table_name,
                    "source_csv": relative_csv_path,
                    "row_count": row_count,
                }
            )

        create_indexes(conn)

        table_counts = get_table_counts(conn)

    return {
        "database_path": database_path,
        "load_results": pd.DataFrame(load_results),
        "table_counts": table_counts,
    }