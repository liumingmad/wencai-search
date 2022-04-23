var block_map = new Map();

$(function () {
    var token = localStorage.getItem('token');
    console.log(token);
    if (!token) {
        goLoginPage();
        return;
    }
    goMainPage();
});

function onClickDownloadCSV() {
    $('.loader').css("visibility", "visible");
    $.ajax('/wencai/basefilter', {
        method: 'GET',
        headers: {
            'token': localStorage.getItem('token')
        },
        dataType: 'text'

    }).done(function (data) {
        console.log('成功, 收到的数据: ' + data);
        var a = $('#download_csv');
        a.css('visibility', 'visible');

    }).fail(function (xhr, status) {
        console.log('失败 ' + status);
        alert("生成失败")

    }).always(function () {
        $('.loader').css("visibility", "hidden");
    }); 
}

function goLoginPage() {
    switchUI('login');
    $('#login_status').css("visibility", "hidden");
}

function goMainPage() {
    switchUI('main');
    getBlockList();
    addClickListener();
}

function onClickLoginBtn() {
    login($('#password').val());
}

function switchUI(tab) {
    $('.login').addClass('login_hidden')
    $('.main').css("visibility", "hidden");
    if (tab == 'main') {
        $('.main').css("visibility", "visible");
    } else {
        $('.login').removeClass('login_hidden');
    }
}

function login(info) {
    var sec = CryptoJS.HmacSHA1('Helloworld!', info).toString();
    $.ajax('/wencai/login?token=' + sec, {
        method: 'GET',
        dataType: 'text'

    }).done(function (data) {
        console.log('成功, 收到的数据: ' + data);
        if (data.length > 0) {
            localStorage.setItem("token", data);
        }
        goMainPage();

    }).fail(function (xhr, status) {
        goLoginPage();
        $('#login_status').css("visibility", "visible");
        console.log('登陆失败 ' + status);

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

function getBlockList() {
    $('.loader').css("visibility", "visible");
    var jqxhr = $.ajax('/wencai/blocklist', {
        method: 'GET',
        headers: {
            'token': localStorage.getItem('token')
        },
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

function getBlockData(sn) {
    $('.loader').css("visibility", "visible");
    var jqxhr = $.ajax('/wencai/block?sn='+sn, {
        method: 'GET',
        headers: {
            'token': localStorage.getItem('token')
        },
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

