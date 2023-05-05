$(document).ready(function () {

    var fd = new FormData();
    var files;  // file lấy được từ input file

    // click remove BG lần đầu
    document.getElementById("btn_submit_image").addEventListener('click', function (e) {
        e.preventDefault();
        files = $('#chosse_image')[0].files;
        // kiểm tra file đã được chọn hay chưa
        if (files.length > 0) {
            //image như là name của tag input nhận được bên file upload
            fd.append('image_input', files[0]);
            $.ajax({
                url: "http://127.0.0.1:8000/removeBG_act?bg_color=255",
                type: "POST",
                data: fd,
                contentType: false,
                processData: false,
                success: function (response) {
                    $('.loading').hide()
                    console.log("link hình ảnh vào " + response['path_img_input']);
                    console.log("link hình ảnh kết quả " + response['path_img_result']);
                    // cho thẻ có id body-main thành trống
                    $("#body-main").html("");
                    $("#body-main").append(
                        "<div class='body-main-top'>" +
                        "<div class='wrap-border'>" +
                        "<div class='list_color_BG' data-colorbg='" + 999 + "'>" +
                        "<div class='bg background-transparent'>" +
                        "<span class='explain-text'>BG trong suốt</span>" +
                        "<div class='arrow'></div>" +
                        "</div>" +
                        "</div>" +
                        "</div>" +
                        "<div class='wrap-border active'>" +
                        "<div class='list_color_BG' data-colorbg='" + 255 + "'>" +
                        "<div class='bg background-white'>" +
                        "<span class='explain-text'>BG trắng</span>" +
                        "<div class='arrow'></div>" +
                        "</div>" +
                        "</div>" +
                        "</div>" +
                        "<div class='wrap-border'>" +
                        "<div class='list_color_BG' data-colorbg='" + 0 + "'>" +
                        "<div class='bg background-black'>" +
                        "<span class='explain-text'>BG đen</span>" +
                        "<div class='arrow'></div>" +
                        "</div>" +
                        "</div>" +
                        "</div>" +
                        "</div>" +
                        "<div class='body-main-body'>" +
                        "<img src='" + response['path_img_result'] + "' class='frame-image'>" +
                        "<div class='loading loading_image' style='display: none;'>" +
                        "<i class='fa-solid fa-spinner'></i>" +
                        "</div>" +
                        "</img>" +
                        "<div class='btn-add-img' id='select-image-btn'>" +
                        "<i class='fa-solid fa-plus'></i>" +
                        "<br/>" +
                        "<br/>" +
                        "<p>Chọn ảnh</p>" +
                        "</div>" +
                        "</div>" +
                        "<div class='body-main-bottom'>" +
                        "<a href='#' class='btn btn-dowload'>" +
                        "Tải ảnh" +
                        "</a>" +
                        "<a href='#' class='btn btn-close'>" +
                        "Đóng tất cả " +
                        "</a>" +
                        "</div>"
                    );

                    removeBG_2()
                    submit_form()

                },
                error: function () {
                    alert("Lỗi");
                }
            });
        } else {
            alert("Please select a file.");
        }
    });

    function removeBG_2() {
        // click remove lần 2
        const buttons_colorBG = document.querySelectorAll(".list_color_BG");

        for (let i = 0; i < buttons_colorBG.length; i++) {
            buttons_colorBG[i].addEventListener('click', function (e) {
                $('.loading.loading_image').show()
                console.log("đã click ")
                console.log($(this).data('colorbg'))
                e.preventDefault();
                // kiểm tra file đã được chọn hay chưa
                if (files.length > 0) {
                    $.ajax({
                        url: "http://127.0.0.1:8000/removeBG_act?bg_color="+ $(this).data('colorbg'),
                        type: "POST",
                        data: fd,
                        contentType: false,
                        processData: false,
                        success: function (response) {
                            $('.loading').hide()
                            console.log("link hình ảnh vào " + response['path_img_input']);
                            console.log("link hình ảnh kết quả " + response['path_img_result']);
                            // cho thẻ có id body-main thành trống
                            $("#body-main").html("");
                            $("#body-main").append(
                                "<div class='body-main-top'>" +
                                "<div class='wrap-border'>" +
                                "<div class='list_color_BG' data-colorbg='" + 999 + "'>" +
                                "<div class='bg background-transparent'>" +
                                "<span class='explain-text'>BG trong suốt</span>" +
                                "<div class='arrow'></div>" +
                                "</div>" +
                                "</div>" +
                                "</div>" +
                                "<div class='wrap-border active'>" +
                                "<div class='list_color_BG' data-colorbg='" + 255 + "'>" +
                                "<div class='bg background-white'>" +
                                "<span class='explain-text'>BG trắng</span>" +
                                "<div class='arrow'></div>" +
                                "</div>" +
                                "</div>" +
                                "</div>" +
                                "<div class='wrap-border'>" +
                                "<div class='list_color_BG' data-colorbg='" + 0 + "'>" +
                                "<div class='bg background-black'>" +
                                "<span class='explain-text'>BG đen</span>" +
                                "<div class='arrow'></div>" +
                                "</div>" +
                                "</div>" +
                                "</div>" +
                                "</div>" +
                                "<div class='body-main-body'>" +
                                "<img src='" + response['path_img_result'] + "' class='frame-image'>" +
                                "<div class='loading loading_image' style='display: none;'>" +
                                "<i class='fa-solid fa-spinner'></i>" +
                                "</div>" +
                                "</img>" +
                                "<div class='btn-add-img' id='select-image-btn'>" +
                                "<i class='fa-solid fa-plus'></i>" +
                                "<br/>" +
                                "<br/>" +
                                "<p>Chọn ảnh</p>" +
                                "</div>" +
                                "</div>" +
                                "<div class='body-main-bottom'>" +
                                "<a href='#' class='btn btn-dowload'>" +
                                "Tải ảnh" +
                                "</a>" +
                                "<a href='#' class='btn btn-close'>" +
                                "Đóng tất cả " +
                                "</a>" +
                                "</div>"
                            );
                            removeBG_2()
                            submit_form()

                        },
                        error: function () {
                            alert("Lỗi");
                        }
                    });
                } else {
                    alert("Please select a file.");
                }
            });
        }

    }


    function submit_form(){
    // chọn được file ảnh thì bắt đầu submit form
    // click vào một nút thì tự động ấn chọn file ảnh và ấn submit
        if (document.getElementById("select-image-btn")) {
            document.getElementById("select-image-btn").addEventListener('click', function () {
                const btn_submit = document.getElementById("btn_submit_image");
                const fileInput = document.getElementById("chosse_image");
                fileInput.click();
                fileInput.onchange = function () {
                    if (fileInput.files.length > 0) {
                        var file = fileInput.files[0];
                        // Thực hiện hành động JavaScript trên tệp đã chọn ở đây
                        // console.log('Bạn đã chọn tệp ' + file.name);
                        btn_submit.click();
                        if($('.loading.loading_image').length){
                            $('.loading.loading_image').show()
                        }else{
                            $('.loading').show();
                        }
                    }
                }
            })
        }
    }
    // để chạy khi người dùng sử dụng removebg lần đầu
    submit_form()

});