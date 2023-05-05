$(document).ready(function (){

    var fd = new FormData();   // để lấy file từ form
    var files;  // file lấy được từ input file



    // nhấn nút chọn ảnh chủ thể
    var btn_img_blur = document.getElementById('btn_img_blur')   // nút chọn ảnh
    var input_img_blur = document.getElementById('input_img_blur')   // input type = file
    var btn_submit_blur = document.querySelector("#btn_submit_blur") // nút submit
    var show_imgBlur_input = document.querySelector("#show_imgBlur_input") // để hiển thị ảnh vừa chọn vào thẻ img

    // click vào nút, tự động click nút input để chọn ảnh, khi chọn ảnh xong thì từ động nhấn nút submit
    btn_img_blur.addEventListener('click', function () {
        input_img_blur.click()
        // sẽ tự động submit form khi đã chọn file ảnh 
        input_img_blur.addEventListener('change', (event) => {
            $('.loading').show()
            // xử lý gửi dữ liệu lên API server theo phương thức post
            files = $('#input_img_blur')[0].files;
            if (files.length > 0) {
                // thêm vào đối tượng FormData (input_img_blur: file đã chọn)
                //image như là name của tag input nhận được bên file upload
                fd.append('input_img_blur', files[0]);
                $.ajax({
                    url: "http://127.0.0.1:8000/blurBG_act",
                    type: "POST",
                    data: fd,
                    contentType: false,
                    processData: false,
                    success: function (response) {
                        $('.loading').hide()
                        console.log("Chức năng làm mờ nền ảnh")
                        console.log("link hình ảnh vào " + response['path_img_input']);
                        console.log("link hình ảnh kết quả " + response['path_img_result']);
                        $("#show_imgBlur_input").attr("src", response['path_img_input'])
                        $("#img_blur_result").attr("src", response['path_img_result'])
                    },
                    error: function () {
                        $('.loading').hide()
                        alert("Lỗi");
                    }
                });
            } else {
                alert("Please select a file.");
            }
        });
    })

    
   


});