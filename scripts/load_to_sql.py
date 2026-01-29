import pandas as pd
import sqlite3
import os

# Define paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
SQL_DIR = os.path.join(PROJECT_ROOT, 'sql')
CSV_FILE = os.path.join(DATA_DIR, 'cleaned_data.csv')
DB_FILE = os.path.join(SQL_DIR, 'ecommerce.db')

def load_data():
    """Loads cleaned data from CSV to SQLite database."""
    
    # Check if CSV exists
    if not os.path.exists(CSV_FILE):
        print(f"Error: CSV file not found at {CSV_FILE}")
        return

    # Create SQL directory if it doesn't exist
    if not os.path.exists(SQL_DIR):
        print(f"Creating SQL directory at {SQL_DIR}")
        os.makedirs(SQL_DIR)

    print(f"Loading data from {CSV_FILE}...")
    try:
        df = pd.read_csv(CSV_FILE)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    print(f"Connecting to database at {DB_FILE}...")
    try:
        conn = sqlite3.connect(DB_FILE)
        
        # Write to SQL
        df.to_sql('sales', conn, if_exists='replace', index=False)
        
        # Verify
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) FROM sales")
        rows = cursor.fetchone()[0]
        
        print(f"Success! Loaded {rows} rows into table 'sales'.")
        
        conn.close()
        
    except Exception as e:
        print(f"Error checking database: {e}")

if __name__ == "__main__":
    load_data()
