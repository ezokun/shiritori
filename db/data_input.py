"""
辞書DBのデータ登録
Mecabおよびmecab-ipadic-NEologdから
名詞系のcsvを取得して実行する必要がある
"""
import sqlite3
import csv

# 変換用リスト
# 実装方式が違うのでリストの持ち方も違う
# 上のほうが早いが面倒だったのでとりあえずの実装
LARGE_LIST = {'ァ': 'ア', 'ィ': 'イ', 'ゥ': 'ウ', 'ェ': 'エ', 'ォ': 'オ',
              'ッ': 'ツ', 'ャ': 'ヤ', 'ュ': 'ユ', 'ョ': 'ヨ', 'ヮ': 'ワ'}
CLEAN_LIST = ['ヴガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポヷヸヹヺ',
              'ウカキクケコサシスセソタチツテトハヒフヘホハヒフヘホワヰヱヲ']
LONG_LIST = ['アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホ' + \
             'マミムメモヤユヨラリルレロワヰウヱヲンヴガギグゲゴザジズゼゾ' + \
             'ダヂヅデドバビブベボヷヸヹヺパピプペポァィゥェォッャュョヮー',
             'アイウエオアイウエオアイウエオアイウエオアイウエオアイウエオ' + \
             'アイウエオアウオアイウエオアイウエオンウアイウエオアイウエオ' + \
             'アイウエオアイウエオアイエオアイウエオアイウエオウアウオアー']

def enlarge(convert_word):
    """
    小書き文字変換
    """
    if convert_word in LARGE_LIST.keys():
        return LARGE_LIST[convert_word]
    return convert_word

def cleaning(convert_word):
    """
    濁音・半濁音変換
    """
    # 走査を2回かけるので相対的には遅い
    if convert_word in CLEAN_LIST[0]:
        return CLEAN_LIST[1][CLEAN_LIST[0].index(convert_word)]
    return convert_word

def change_long(convert_word):
    """
    長音をア行に変換
    """
    return LONG_LIST[1][LONG_LIST[0].index(convert_word)]

def main():
    """
    メイン
    """
    # DBファイル名
    dbname = 'word_neologd.sqlite3'
    # DB接続・カーソル取得
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()

    # 挿入用SQL
    insert_sql = 'INSERT INTO ' + \
                    'word (name, reading, count, ' + \
                    'first, last, first_clean, last_large, last_clean, ' + \
                    'last_large_long, last_clean_long, cost) ' + \
                    'VALUES (?,?,?,?,?,?,?,?,?,?,?)'

    file_list = ['./data/Noun.adjv.csv',
                 './data/Noun.adverbal.csv',
                 './data/Noun.csv',
                 './data/Noun.verbal.csv',
                 './data/Noun.demonst.csv',
                 './data/Noun.nai.csv',
                 './data/Noun.name.csv',
                 './data/Noun.number.csv',
                 './data/Noun.org.csv',
                 './data/Noun.others.csv',
                 './data/Noun.place.csv',
                 './data/Noun.proper.csv']
    # file_list = ['./data/mecab-user-dict-seed.20180920.csv']

    for one_file in file_list:
        # ファイルオープン
        print(one_file)
        with open(one_file, 'r', encoding='euc-jp') as csvfile:
        # with open(one_file, 'r', encoding='utf8') as csvfile:
            # csvファイル読み込み
            csv_reader = csv.reader(csvfile, delimiter=',')
            # 行取得
            for row in csv_reader:
                # とりあえず名詞だけ取得
                if row[4] != '名詞':
                    continue

                # 先頭文字を清音に
                first_clean = cleaning(enlarge(row[11][0]))

                # 末尾の長音をはずす
                last_word = row[11][-1] if row[11][-1] != 'ー' else row[11][-2]

                # 末尾の小書き文字を変換
                # 拗音を1文字とするルールには未対応
                #   その場合文字数はどうなるんだろ
                last_large = enlarge(last_word)

                # 末尾文字を清音に
                # 拗音対応する場合は2カラム追加が必要
                last_clean = cleaning(last_large)

                # 末尾の長音を変換する
                last_large_long = last_large if row[11][-1] != 'ー' else change_long(row[11][-2])
                last_clean_long = last_clean if row[11][-1] != 'ー' else change_long(row[11][-2])

                # DB登録
                word = (row[0], row[11], len(row[11]),
                        row[11][0], row[11][-1],
                        first_clean, last_large, last_clean,
                        last_large_long, last_clean_long, int(row[3]))

                # 重複エラーは除く
                try:
                    cur.execute(insert_sql, word)
                except sqlite3.IntegrityError:
                    pass
                    #print("重複")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
