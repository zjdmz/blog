//  添加分类 弹窗编辑
$(function () {
    var add_cat = $('#add_category');
    add_cat.click(function () {
        swal({
            title: '请输入分类名称',
            content: 'input',
            buttons: ['取 消', '提 交']
        }).then((value) => {
            if(value) {
                $.ajaxSetup({
                    beforeSend: function (xhr, settings) {
                        if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type) && !this.crossDomain) {
                            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                        }
                    }
                });
                $.ajax({
                    //几个参数需要注意一下
                    type: "POST",//方法类型
                    dataType: "json",//预期服务器返回的数据类型
                    url: "/edit_category",
                    data: {"category": value, 'code': 'add'},
                    success: function (result) {
                        console.log(typeof (result));//打印服务端返回的数据(调试用)
                        var result_message = result["message"];
                        if (result_message) {
                            swal({
                                title: "创建分类成功!",
                                text: "创建的分类：" + result_message.toString(),
                                timer: 1500,
                                button: false
                            }).then(() => {window.location.reload()
                        })
                            ;
                        } else {
                            swal({
                                title: '创建失败',
                                timer: 1500,
                                button: false
                            })
                        }
                    },
                    error: function () {
                        window.messageBox.showError("异  常！")
                    }
                });
            };
        })
    });
});

// 编辑分类
$(function () {
    var editBtn = $('.edit_ctg');
    editBtn.click(function () {
        var currentBtn = $(this);
        var tr = currentBtn.parent().parent();
        var pk = tr.attr('ctg-id');
        var ctgName = tr.attr('ctg-name');

        swal({
            title: '编辑分类',
            content: {
                element: 'input',
                attributes: {
                    value: ctgName,
                    type: "text",
                }
            },
            buttons: ['取 消', '提 交']
        }).then((value) => {
            if(value){
                $.ajaxSetup({
                    beforeSend: function (xhr, settings) {
                        if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type) && !this.crossDomain) {
                            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                        }
                    }
                });
                $.ajax({
                    //几个参数需要注意一下
                    type: "POST",//方法类型
                    dataType: "json",//预期服务器返回的数据类型
                    url: "/edit_category",
                    data: {"category": value, 'code': 'edit', 'ctg_id': pk},
                    success: function (result) {
                        console.log(typeof (result));//打印服务端返回的数据(调试用)
                        var result_message = result["message"];
                        if (result_message) {
                            swal({
                                title: "修改分类成功!",
                                text: "修改后的分类：" + result_message.toString(),
                                timer: 1500,
                                button: false
                            }).then((value) => {window.location.reload()
                        })
                        } else {
                            swal({
                                title: '创建失败',
                                timer: 1500,
                                button: false
                            })
                        }
                    },
                    error: function () {
                        window.messageBox.showError("异  常！")
                    }
                });
            }
        });
    });
});


//  删除分类
$(function () {
    var delBtn = $(".del_ctg");
    delBtn.click(function () {
        var currentBtn = $(this);
        var tr = currentBtn.parent().parent();
        var ctg_id = tr.attr('ctg-id');
        var ctg_name = tr.attr('ctg-name');
        swal({
            title:'删除分类？',
            text:ctg_name,
            buttons:['取 消','删 除'],
            dangerMode: true,
        }).then((willDelete) => {
                if(willDelete) {
                    $.get({
                        'url': "/del_category",
                        dataType: "json",//预期服务器返回的数据类型
                        'data': {"category": ctg_name, 'code': 'del', 'ctg_id': ctg_id},
                        'success': function (result) {
                            if (result['message'] === 'ok') {
                                swal({
                                    title: '删除分类成功',
                                    text: ctg_name,
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


