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
    cur.execute('delete from HISTORY')
    cur.execute('delete from COUNT')
    cur.execute('insert into HISTORY values(?)', ('シリトリ',))
    cur.execute('insert into COUNT values(?, ?)', ('リ', '1'))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()
