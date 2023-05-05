$(document).ready(function (){

    // để xử lý khi chọn file và gửi lên http server
    var fd = new FormData();
    var files;

    var input_img_gray = $("#input_img_gray")   // input file
    var btn_img_gray = $("#btn_img_gray")    // btn để nhấn
    var btn_submit_gray = $("#btn_submit_gray")// btn submit
    var img_blur_result = $("#img_blur_result")// img show result
    var show_imgBlur_input = $("#show_imgBlur_input")// img show input

    btn_img_gray.on("click", function(){
        input_img_gray.click()
    })
    
    // khi đã chọn 1 ảnh từ form chọn ảnh
    input_img_gray.on("change", function(){
        $('.loading').show()
        files = $('#input_img_gray')[0].files;
        if(files.length > 0){
            fd.append('input_img_gray', files[0])
            $.ajax({
                url: "http://127.0.0.1:8000/grayBG_act",
                type: "post",
                data: fd,
                contentType: false,
                processData: false,
                success: function(response){
                    $('.loading').hide()
                    console.log("path_img_old: "+ response['path_img_old'])
                    console.log("path_img_result: "+ response['path_img_result'])
                    show_imgBlur_input.attr("src", response['path_img_old'])
                    img_blur_result.attr("src", response['path_img_result'])
                },
                error: function(){
                    $('.loading').hide()
                    alert("Lỗi");
                }
            })
        }
    })

});