import sqlite3, json, time

def log_to_db(node_id, payload, db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # 1. insert/update node last_seen
    cur.execute("""
        INSERT OR REPLACE INTO nodes (id, last_seen)
        VALUES (?, ?)
    """, (node_id, time.time()))

    # 2. insert raw data
    cur.execute("""
        INSERT INTO data (node_id, timestamp, raw_value)
        VALUES (?, ?, ?)
    """, (node_id, time.time(), json.dumps(payload)))
    
    conn.commit()
    conn.close()