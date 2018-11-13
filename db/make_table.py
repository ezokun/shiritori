"""
辞書DBの作成
"""
import sqlite3

def main():
    """
    メイン
    """
    # DBファイル名
    dbname = 'word_neologd.sqlite3'
    # dbname = 'word_ipadic.sqlite3'
    # DB接続・カーソル取得
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    create_sql = """
    CREATE TABLE word (
            name TEXT, reading TEXT, count INTEGER NOT NULL, 
            first TEXT NOT NULL, last TEXT NOT NULL,
            first_clean, last_large TEXT NOT NULL, last_clean TEXT NOT NULL,
            last_large_long TEXT NOT NULL, last_clean_long TEXT NOT NULL,
            cost INTEGER NOT NULL,
            PRIMARY KEY(name, reading));
    CREATE INDEX first_index on word(first);
    CREATE INDEX first_count_index on word(first, count);
    CREATE INDEX first_clean_index on word(first_clean);
    CREATE INDEX first_clean_count_index on word(first_clean, count);
    CREATE INDEX word_bascket_index on word(first_clean, last_clean_long, count);
    CREATE INDEX cost_index on word(cost);
    """
    cur.executescript(create_sql)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
