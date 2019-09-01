
$(function () {
    window.editor = KindEditor.create('#editor-id',{
        resizeMode : 1,
    })
});

function articleSub(nid) {
    editor.sync();
    var title = $('#title').val();
    if (!title){
        alert('标题不能为空');
        return 0
    }
    var introduce = $('#introduce').val();
    if (!introduce){
        alert('简介不能为空');
        return 0
    }
    var content = $('#editor-id').val();
    if (!content){
        alert('正文不能为空');
        return 0
    }
    var category = $("input[name='category']:checked").val();
    if (!category){
        alert('分类不能为空');
        return 0
    }
    if (nid) {
        $.ajax({
            url: '/write-article-' + nid + '.html',
            type: 'post',
            headers: {'x-CSRFtoken': $.cookie('csrftoken')},
            data: {
                'title': title,
                'introduce': introduce,
                'content': content,
                'category': category,
            },
            dataType: 'json',
            success: function (arg) {
                if (arg.state) {
                    location.href = '/';
                }
            }
        })
    }else {
        $.ajax({
            url: '/write-article.html',
            type: 'post',
            headers: {'x-CSRFtoken': $.cookie('csrftoken')},
            data: {
                'title': title,
                'introduce': introduce,
                'content': content,
                'category': category,
            },
            dataType: 'json',
            success: function (arg) {
                if (arg.state) {
                    location.href = '/';
                }
            }
        })
    }
}
