TOKEN = ''
var block_map = new Map();


$(function () {
    initUI();
    //getBlockList()
    //addClickListener();
});

function onClickLoginBtn() {
    login($('#password').val());
    // save to local
}

function initUI() {
    var token = window.localStorage.getItem('token');
    console.log(token);
    if (token) {
        switchUI('main');
    } else {
        switchUI('login');
    }
}

function switchUI(tab) {
    $('.login').css("visibility", "hidden");
    $('.main').css("visibility", "hidden");
    if (tab == 'main') {
        $('.main').css("visibility", "visible");
    } else {
        $('.login').css("visibility", "visible");
    }
}

function login(info) {
    $.ajax('/wencai/login?token=' + genToken(info), {
        method: 'GET',
        dataType: 'text'

    }).done(function (data) {
        console.log('成功, 收到的数据: ' + data);
        if (data.length > 0) {
            TOKEN = data;
        }
        switchUI('main');

    }).fail(function (xhr, status) {
        switchUI('login');
        console.log(error);
        alert('登陆失败')

    }).always(function () {
    });
}

function showBlockList(arr) {
    $('#block_list li').remove();
    var blist = $('#block_list');
    for (var i=0; i<arr.length; i++) {
        blist.append('<li>' + arr[i].ln + '</li>')
    }
}

function genBlockMap(arr) {
    var map = new Map();
    map.clear();
    for (var i=0; i<arr.length; i++) {
        var one = arr[i];
        map.set(one.ln, one.sn);
    }
    return map;
}

// http://127.0.0.1:8080/wencai/blocklist
function getBlockList() {
    $('.loader').css("visibility", "visible");
    var jqxhr = $.ajax('/wencai/blocklist', {
        method: 'GET',
        headers: genHeaders(),
        dataType: 'json'

    }).done(function (obj) {
        data = obj.data;
        console.log('成功, 收到的数据: ' + JSON.stringify(data));
        block_map = genBlockMap(data);
        showBlockList(data);
        addClickListener();

    }).fail(function (xhr, status) {
        error = '失败: ' + xhr.status + ', 原因: ' + status
        console.log(error);
        alert(error)

    }).always(function () {
        $('.loader').css("visibility", "hidden");
    });
}

function addClickListener() {
    var list = $('#block_list li');
    for (var i=0; i<list.length; i++) {
        var one = list.get(i);
        one.onclick = function (e) {
            var sn = block_map.get(e.target.innerText);
            getBlockData(sn);
        };
    }
}

// http://127.0.0.1:8080/wencai/block?sn=14B
function getBlockData(sn) {
    $('.loader').css("visibility", "visible");
    var jqxhr = $.ajax('/wencai/block?sn='+sn, {
        method: 'GET',
        headers: genHeaders(),
        dataType: 'text'

    }).done(function (data) {
        console.log('成功, 收到的数据: ' + data);
        $('.stock-table').html(data);

    }).fail(function (xhr, status) {
        error = '失败: ' + xhr.status + ', 原因: ' + status
        console.log(error);
        alert(error)

    }).always(function () {
        $('.loader').css("visibility", "hidden");
    });
}

function genHeaders() {
    headers = {
        'token': TOKEN
    };
    return headers;
}

function genToken(secret) {
    var s = CryptoJS.HmacSHA1('Helloworld!', secret).toString();
    console.log(s);
    return s;
}
