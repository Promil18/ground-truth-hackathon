import polars as pl
import os

def load_csv(filepath: str) -> pl.DataFrame:
    """Loads a CSV file into a Polars DataFrame."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    try:
        df = pl.read_csv(filepath)
        print(f"Successfully loaded {filepath} with shape {df.shape}")
        return df
    except Exception as e:
        print(f"Error loading CSV {filepath}: {e}")
        raise

def load_sql(connection_string: str, query: str) -> pl.DataFrame:
    """
    Loads data from a SQL database into a Polars DataFrame.
    """
    try:
        df = pl.read_database_uri(query=query, uri=connection_string)
        print(f"Successfully loaded data from SQL with shape {df.shape}")
        return df
    except Exception as e:
        print(f"Error loading from SQL: {e}")
        raise
