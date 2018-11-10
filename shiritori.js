var target_char = '';
var count = {};
var hist = [];

$(function(){
    // ボタンクリック時のイベントハンドラ
    $('#ajax').on('click', button_click_event);
    // エンターキー押下でボタンクリック、あとフォーカス当て
    $('#word').on('keypress', (e) => {
        if (e.which === 13) {
            $('#ajax').click();
        }
    }).focus();
    disp_answer('しりとり', 'シリトリ', 'リ');
});

// ボタンクリック時のイベント
function button_click_event() {

    var word = $('#word').val();
    $('#word').val('').focus();

    // 未入力チェック
    if (word === '') {
        return;
    }
    // 履歴チェック
    if (hist.indexOf(word) >= 0) {
        disp_message(word, false);
        disp_message('※「' + word + '」は回答済みです。', true);
        return;
    }
    // Ajax通信1回目：入力単語のチェック
    $.ajax({
        url:'./shiritori.php',
        type:'POST',
        data:{
            'type':'ask',
            'word':word,
            'target':target_char,
        }
    })
    .done(check_word_ajax_done)
    .fail(ajax_fail)
    .always(ajax_always);
}

// Ajaxリクエスト成功：1回目：入力単語チェック
function check_word_ajax_done(data) {
    json_data = $.parseJSON(data)
    // メッセージがあれば表示
    if (json_data['message'] !== undefined) {
        if (json_data['word'] !== undefined) {
            disp_message(json_data['word'], false);
        }
        disp_message(json_data['message'], true);
    }
    else {
        name = json_data['name'];
        reading = json_data['reading'];
        last = json_data['last'];
        // 結果を表示
        disp_message(name + '(' + reading + ') : ' + last, false);

        // 履歴登録
        hist.push(name);
        // 実行回数をセット
        if (count[last] === undefined) {
            count[last] = 0;
        }

        //2回目：文字と回数を元に単語を取得
        $.ajax({
            url:'./shiritori.php',
            type:'POST',
            data:{
                'type':'ans',
                'first':last,
                'count':count[last],
            }
        })
        .done(get_word_ajax_done)
        .fail(ajax_fail)
        .always(ajax_always);

        // 単語取得回数を更新
        count[last]++;
    }
}

// Ajaxリクエスト成功：2回目：単語取得
function get_word_ajax_done(data) {
    json_data = $.parseJSON(data)
    // メッセージがあれば表示
    if (json_data['message'] !== undefined) {
        if (json_data['word'] !== undefined) {
            disp_message(json_data['word'], false);
        }
        disp_message(json_data['message'], true);
    }
    else {
        // 結果を表示
        disp_answer(json_data['name'], json_data['reading'], json_data['last']);
    }
}

// Ajaxリクエスト失敗
function ajax_fail(data) {
    disp_message('※通信に失敗しました', true);
    console.log(data);
}

// Ajaxリクエスト常時
function ajax_always(data) {
}

// 回答を表示
function disp_answer(name, reading, last) {
    disp_message( name + '(' + reading + ') : ' + last, true);
    // 対象文字を更新
    target_char = last;
}

// メッセージ表示
function disp_message(message, isCPU) {
    if (isCPU) {
        message = '<div class="balloon6"><div class="faceicon"><img src="robot.png"></div>' +
        '<div class="chatting"><div class="says"><p>' +
        message + '</p></div></div></div>';
    }
    else {
        message = '<div class="mycomment"><p>' +
        message + '</p></div>';
    }
    $('.result').html(message + '<br>' + $('.result').html());
}