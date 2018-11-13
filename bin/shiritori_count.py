import sys
import sqlite3

def main(check_word):
    dbname = './db/history.sqlite3'
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    # execで連携する場合、文字化けが発生する
    check_word = check_word.encode('cp932')
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
