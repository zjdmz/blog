

//  删除文章
$(function () {
    var delBtn = $(".del_article");
    delBtn.click(function () {
        var currentBtn = $(this);
        var tr = currentBtn.parent().parent();
        var article_id = tr.attr('article-id');
        var article_name = tr.attr('article-name');
        swal({
            title:'删除文章？',
            text:article_name,
            buttons:['取 消','删 除'],
            dangerMode: true,
        }).then((willDelete) => {
                if(willDelete) {
                    $.get({
                        'url': "/del_article",
                        dataType: "json",//预期服务器返回的数据类型
                        'data': {"article": article_name, 'code': 'del', 'article_id': article_id},
                        'success': function (result) {
                            if (result['message'] === 'OK') {
                                swal({
                                    title: '删除文章成功',
                                    text: article_name,
                                    button: false,
                                    timer: 1500
                                }).then((willDelete) => {window.location.reload();
                            });
                            } else {
                                swal('删除失败')
                            }
                        }
                    })
                }
        });
    })
});