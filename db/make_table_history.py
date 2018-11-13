import sqlite3

def main():
    # DBファイル名
    dbname = 'history.sqlite3'
    # DB接続・カーソル取得
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    create_sql = """
    CREATE TABLE COUNT (
            reading TEXT, count INTEGER NOT NULL, 
            PRIMARY KEY(reading));
    """
    cur.executescript(create_sql)
    create_sql = """
    CREATE TABLE HISTORY (
            word TEXT, 
            PRIMARY KEY(word));
    """
    cur.executescript(create_sql)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
