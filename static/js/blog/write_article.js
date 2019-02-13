tinymce.init({
    selector: 'textarea',
    theme: "modern",
    language: "zh_CN",
    plugins: [
        'advlist autolink autosave lists link  charmap print preview anchor',
        'searchreplace visualblocks code fullscreen textcolor colorpicker textpattern code image',
        'contextmenu paste '
    ],
    toolbar1: " bold italic underline strikethrough | alignleft aligncenter alignright alignjustify | fontselect fontsizeselect  forecolor backcolor | bullist numlist | outdent indent | removeformat | link unlink | image undo redo",

    font_formats: '宋体=宋体;仿宋=仿宋;楷体=楷体;黑体=黑体;微软雅黑=微软雅黑;幼圆=幼圆;方正小标宋简体=方正小标宋简体;隶书=隶书;Times new Roman=Times new Roman;华文行楷=华文行楷;华文楷体=华文楷体;华文宋体=华文宋体;华文仿宋=华文仿宋;华文行楷=华文行楷;',
    image_advtab: true,
    paste_data_images: true,
    fontsize_formats: '8pt 9pt 10pt 11pt 12pt 13pt 14pt 15pt 16pt 18pt 20pt 22pt 24pt 26pt 28pt 30pt 32pt 34pt 36pt 38pt 40pt',
    file_browser_callback: function (field_name, url, type, win) {
        $('#my_form input').click();
    }
});


$(document).ready(function () {
    h = '<iframe id="form_target" name="form_target" style="display:none"></iframe><form id="my_form" action="/upload/image" target="form_target" method="post" enctype="multipart/form-data" style="width:0px;height:0;overflow:hidden"><input name="img" type="file" accept="image/gif,image/jpeg,image/jpg,image/png" onchange="$(\'#my_form\').submit();this.value=\'\';" id="article_img">  <input type="text" name="code" value="article_img"> </form>';
    $('body').append(h);

    var csrftoken = getCookie('csrftoken');
    console.log('csrftoken = ' + csrftoken);
    $('#my_form').append('<input type="hidden" name="csrfmiddlewaretoken" value=' + csrftoken + ' />');
});


// 上传文章缩略图
$(document).ready(function () {
    var thumb_input = $('#thumbnail');
    var thumb_button = $("#upload_image");
    // 绑定上传图片按钮和input文件标签
    thumb_button.click(function () {
        thumb_input.click();
    });
});


$(function () {
    var thumb_input = $("#thumbnail");
    var thumb_url = $("#thumb_url");

    //③创建fileLoad方法用来上传文件
    function fileLoad(ele) {
        //④创建一个formData对象
        var formData = new FormData();
        //⑤获取传入元素的val
        console.log('ele = ' + ele);
        var name = $(ele).val();
        //⑥获取files
        var files = $(ele)[0].files[0];
        //⑦将name 和 files 添加到formData中，键值对形式
        formData.append("img", files);
        formData.append("code", 'thumb_img');
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            }
        });
        $.ajax({
            url: "/upload/image",
            type: 'POST',
            data: formData,
            processData: false,// ⑧告诉jQuery不要去处理发送的数据
            contentType: false, // ⑨告诉jQuery不要去设置Content-Type请求头
            success: function (result) {
                if (result.status === 200) {
                    window.messageBox.showSuccess('上传成功');
                    console.log(result.thumb_img);
                    thumb_url.attr('value', result.thumb_img);  // 11成功后的动作
                } else {
                    window.messageBox.showError(result.type_error);
                }
            }
            ,
            error: function (result) {
                window.messageBox.showError('上传失败');  // 12出错后的动作
            }
        });
    }

    // ①为input设定change事件
    thumb_input.change(function upload_thumb() {
        //    ②如果value不为空，调用文件加载方法
        var filename = thumb_input.val().split('.');
        var file_ext = filename[filename.length - 1];
        console.log(file_ext);
        if (['png', 'jpeg', 'jpg', 'gif'].indexOf(file_ext) !== -1) {
            if (thumb_input.val() !== "") {
                fileLoad(thumb_input);
            }
        } else {
            window.messageBox.showError('文件类型错误');
        }
    })
});

$(function () {
    var addBtn = $(".add_category");
    addBtn.click(function () {
        window.location.href = '/edit_category';
    })
});

















