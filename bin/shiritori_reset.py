"""
履歴DBリセット
"""
import sqlite3

def main():
    """
    メイン
    """
    dbname = './db/history.sqlite3'
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute('DELETE FROM HISTORY')
    cur.execute('DELETE FROM COUNT')
    cur.execute('INSERT INTO HISTORY VALUES(?)', ('シリトリ',))
    cur.execute('INSERT INTO COUNT VALUES(?, ?)', ('リ', '1'))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()
