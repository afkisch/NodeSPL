import sqlite3

def create_node_table(db_path):
    # Connect to the SQLite database (or create it if it doesn't exist)
    connection_obj = sqlite3.connect(db_path)

    # Create a cursor object to interact with the database
    cursor_obj = connection_obj.cursor()

    # Drop the GEEK table if it already exists (for clean setup)
    #cursor_obj.execute("DROP TABLE IF EXISTS nodes")
    #cursor_obj.execute("DROP TABLE IF EXISTS data")

    # Execute the table creation query
    cursor_obj.execute("""
    -- table of nodes
    CREATE TABLE IF NOT EXISTS nodes (
        id TEXT PRIMARY KEY,
        last_seen TIMESTAMP
    );
    """)
    cursor_obj.execute("""
    -- raw data log
    CREATE TABLE IF NOT EXISTS data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        node_id TEXT NOT NULL,
        timestamp TIMESTAMP NOT NULL,
        raw_value TEXT NOT NULL,   -- JSON dump of node input
        FOREIGN KEY(node_id) REFERENCES nodes(id)
    );
    """)

    # Confirm that the table has been created
    print("Table is Ready")

    # Close the connection to the database
    connection_obj.close()