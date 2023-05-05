$(document).ready(function () {

    window.addEventListener('beforeunload', function (event) {
        event.preventDefault(); // Ngăn chặn việc tải lại trang
        event.returnValue = ''; // Gán chuỗi rỗng cho returnValue để hiển thị thông báo xác nhận
    });

    // để xử lý khi chọn file và gửi lên http server
    var fd = new FormData();
    var files_subject;
    var files_bg;


    // nhấn nút chọn ảnh chủ thể
    var btn_img_subject = $('#btn_img_subject')   // btn chọn ảnh subject
    var input_img_subject = $('#input_img_subject')  // input file ảnh subject
    btn_img_subject.on('click', function () {
        input_img_subject.click()
    })

    // nhấn nút chọn ảnh nền
    var btn_img_bg = $('#btn_img_bg')  // btn chọn ảnh nền
    var input_img_bg = $('#input_img_bg')  // input file ảnh nền
    btn_img_bg.on('click', function () {
        input_img_bg.click()
    })

    input_img_subject.on("change", function (event) {
        files_subject = $('#input_img_subject')[0].files;
        fd.append('img_subject', files_subject[0])

        const file_subject = event.target.files[0];
        const reader_subject = new FileReader();
        reader_subject.onload = (e1) => {
            $("#show_img_subject").attr("src", e1.target.result)
        };
        reader_subject.readAsDataURL(file_subject);

        input_img_bg.on("change", function (event2) {
            files_bg = $("#input_img_bg")[0].files;
            fd.append('img_bg', files_bg[0]);

            const file_bg = event2.target.files[0];
            const reader_bg = new FileReader();
            reader_bg.onload = (e2) => {
                $("#show_img_bg").attr("src", e2.target.result)
            };
            reader_bg.readAsDataURL(file_bg);
            // alert("đã chọn 2 ảnh")
            if (files_subject.length > 0 && files_bg.length > 0) {
                // alert("OK")
                $('.loading').show()
                $.ajax({
                    url: "http://127.0.0.1:8000/changeBG_act",
                    type: "post",
                    data: fd,
                    contentType: false,
                    processData: false,
                    success: function (response) {
                        console.log("path_img_input_subject " + response['path_img_input_subject'])
                        console.log("path_img_input_bg " + response['path_img_input_bg'])
                        console.log("path_img_result " + response['path_img_result'])
                        // reset lại img hiển thị ảnh lúc vừa chọn
                        $("#show_img_subject").attr("src", "./assets/image/image_background.png")
                        $("#show_img_bg").attr("src", "./assets/image/image_background.png")

                        // hiển thị ảnh kết quả, 2 ảnh trước khi xử lý 
                        $('#show_img_subject_old').attr("src", response['path_img_input_subject'])
                        $('#show_img_bg_old').attr("src", response['path_img_input_bg'])
                        $('#show_img_changeBG').attr("src", response['path_img_result'])
                        $('.loading').hide()
                        $('#wrap_box_img').show()

                        // hiển thị nút tải ảnh
                        $(".body-main-bottom").show()
                        // tạo link cho nút tải xuống
                        $("#btn-dowload").attr("href", response['path_img_result'])
                    },
                    error: function () {
                        alert("lỗi rồi")
                        $(".loading").hide()
                    }
                })
            }
        })
    })
});