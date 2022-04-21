$(function () {
    addClickListener();
});

function addClickListener() {
    var list = $('#block_list li');
    for (var i=0; i<list.length; i++) {
        var one = list.get(i);
        one.onclick = function (e) {
            console.log(e.target.innerText);
        };
    }
}