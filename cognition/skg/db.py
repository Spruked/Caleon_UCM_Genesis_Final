import sqlite3, json, os, pathlib
DB_FILE = pathlib.Path(os.environ.get("UCM_SKG_DB", "ucm_skg.db"))

def conn():
    DB_FILE.parent.mkdir(exist_ok=True)
    return sqlite3.connect(DB_FILE)

def init_db():
    c = conn()
    c.execute("CREATE TABLE IF NOT EXISTS triples"
              "(sub TEXT, pred TEXT, obj TEXT, weight REAL)")
    c.commit(); c.close()

def add_triple(s, p, o, w=1.0):
    c = conn()
    c.execute("INSERT INTO triples VALUES (?,?,?,?)", (s, p, o, w))
    c.commit(); c.close()

def query_pattern(pat, k=10):
    # pat = [sub,pred,obj]  None = wildcard
    c = conn()
    sql, args = "SELECT * FROM triples WHERE 1=1", []
    for idx, col in enumerate(["sub", "pred", "obj"]):
        if pat[idx] is not None:
            sql += f" AND {col}=?"
            args.append(pat[idx])
    rows = c.execute(sql, args).fetchall()
    c.close()
    return rows[:k]