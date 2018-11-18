<?php
$return_array = [];
// 処理種別で切り分け
if (!isset($_POST['type'])) {
    $return_array['error'] = '*no type error';
}
else {
    // 単語の存在チェック
    if (strcmp($_POST['type'], 'ask') === 0) {
        if (!isset($_POST['word']) or !isset($_POST['target'])) {
            $return_array['error'] = '*no word error';
        }
        else {
            $return_array = check_word($_POST['word'], $_POST['target']);
        }
    }
    // 解答取得
    elseif (strcmp($_POST['type'], 'ans') === 0) {
        if (!isset($_POST['first'])) {
            $return_array['error'] = '*no param error';
        }
        else {
            $return_array = get_word($_POST['first']);
        }
    }
    // リセット
    elseif (strcmp($_POST['type'], 'rst') === 0) {
        exec('python ./bin/shiritori_reset.py');
    }
}
// 返信
header('Content-Type: text/javascript; charset=utf-8');
echo(json_encode($return_array));


// 対象の単語から読みを取得する
function check_word($word, $target)
{
    $return_array = NULL;
    try {
        // データ取得
        $sql = 'SELECT name, reading, first_clean, last_clean_long '.
                'FROM word WHERE name = ? order by cost';
        $pdo = new PDO('sqlite:' . __DIR__ . DIRECTORY_SEPARATOR . 'db' . DIRECTORY_SEPARATOR . 'word_ipadic.sqlite3');
        // $pdo = new PDO('sqlite:' . __DIR__ . DIRECTORY_SEPARATOR . 'db' . DIRECTORY_SEPARATOR . 'word_neologd.sqlite3');
        $stmt = $pdo->prepare($sql);
        $stmt->execute([$word]);
        $results = $stmt->fetchAll();
    }
    catch (Exception $e) {
    }

    // 結果なし
    if (count($results) === 0) {
        $return_array['message'] = '※その言葉は知りません。: ' . 
                htmlspecialchars($_POST['word'], ENT_QUOTES);
        $return_array['word'] = htmlspecialchars($_POST['word'], ENT_QUOTES);
        return $return_array;
    }

    // 読みを検索し、対象の文字から始まる単語を取得
    $last_nn = FALSE;
    $history_exist = FALSE;
    foreach ($results as $result) {
        if (strcmp($target, $result['first_clean']) === 0) {
            // 「ん」で終わる読み方の場合
            if (strcmp('ン', $result['last_clean_long']) === 0) {
                $last_nn = TRUE;
                $return_array['reading'] = $result['reading'];
            }
            else {
                $last_nn = FALSE;
                // 履歴チェック
                exec('python ./bin/shiritori_history.py ' . 
                        $result['reading'],
                        // mb_convert_encoding($result['reading'], "CP932"),
                        $history_count);
                // 履歴にない場合は取得して検索終了
                if ($history_count[0] == 0) {
                    $history_exist = FALSE;
                    $return_array['name'] = $result['name'];
                    $return_array['reading'] = $result['reading'];
                    $return_array['last'] = $result['last_clean_long'];
                    break;
                }
                else {
                    $history_exist = TRUE;
                    $return_array['reading'] = $result['reading'];
                    $return_array['history_count'] = $history_count;
                }
            }
        }
    }

    if ($last_nn) {
        $return_array['message'] = '※「' . 
                htmlspecialchars($_POST['word'], ENT_QUOTES) .
                '(' . $return_array['reading'] . ')' .
                '」の読みは「ン」で終わります。';
        $return_array['word'] = htmlspecialchars($_POST['word'], ENT_QUOTES);
    }
    elseif ($history_exist) {
        $return_array['message'] = '※「' . 
                htmlspecialchars($_POST['word'], ENT_QUOTES) .
                '(' . $return_array['reading'] . ')' .
                '」は使用済みです。';
        $return_array['word'] = htmlspecialchars($_POST['word'], ENT_QUOTES);
    }
    elseif ($return_array === NULL) {
        $return_array['message'] = '※「' . $target .
                '」で始まる読み方を知りません。: ';
        $return_array['word'] = htmlspecialchars($_POST['word'], ENT_QUOTES);
    }

    return $return_array;
}

// 指定した文字で始まる単語を、
// 取得回数に応じて取得する
function get_word($first) {
    $return_array = NULL;

    while(TRUE) {
        // 指定文字のDB取得回数
        exec('python ./bin/shiritori_count.py ' . 
                $first, $count);
                // mb_convert_encoding($first, "CP932"), $count);
        try {
            // データ取得
            $sql = 'SELECT name, reading, first_clean, last_clean_long '. 
                    'FROM word WHERE first_clean = ? ' .
                    'order by cost limit 1 offset ?';
            $pdo = new PDO('sqlite:' . __DIR__ . DIRECTORY_SEPARATOR . 'db' . DIRECTORY_SEPARATOR . 'word_ipadic.sqlite3');
            $stmt = $pdo->prepare($sql);
            $stmt->execute([$first, $count[0]]);
            $results = $stmt->fetchAll();
        }
        catch (Exception $e) {
        }

        // 結果なし
        if (count($results) === 0) {
            $return_array['message'] = '※「' + $first + 
                    '」で始まる言葉をもう知りません。私の負けです。'; 
            break;
        }

        $result = $results[0];

        // 履歴チェック
        exec('python ./bin/shiritori_history.py ' . 
                $result['reading'],
//                mb_convert_encoding($result['reading'], "CP932"),
                $history_count);

        if ($history_count[0] == 0) {
            $return_array['name'] = htmlspecialchars($result['name'], ENT_QUOTES);
            $return_array['reading'] = $result['reading'];
            $return_array['last'] = $result['last_clean_long'];
            break;
        }
    }
    return $return_array;
}