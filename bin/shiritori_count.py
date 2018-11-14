"""
指定した文字の取得位置を取得し、一つカウントアップする
"""
import sys
import sqlite3

def main(check_word):
    """
    メイン
    """
    dbname = './db/history.sqlite3'
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    results = cur.execute('select count from COUNT where reading = ?', (check_word,))
    result = results.fetchone()
    if result is None:
        count = 0
        cur.execute('insert into COUNT values(?, ?)', (check_word, 1))
    else:
        count = result[0]
        cur.execute('update COUNT set count = ? where reading = ?', (count+1, check_word))

    conn.commit()
    conn.close()
    print(count)


if __name__ == '__main__':
    main(sys.argv[1])
