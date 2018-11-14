"""
単語履歴DBの検索および登録
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
    results = cur.execute('SELECT COUNT(word) FROM HISTORY WHERE word = ?', (check_word,))
    count = results.fetchone()[0]
    if count == 0:
        cur.execute('INSERT INTO HISTORY VALUES(?)', (check_word,))
        conn.commit()
    conn.close()
    print(count)


if __name__ == '__main__':
    main(sys.argv[1])
