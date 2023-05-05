import requests

# Dữ liệu để tạo một bài đăng mới
data = {
    "path_input": "C:\\Users\\Tin Ngo\\Desktop\\imageTest\\red-car.png"
}

# Gửi yêu cầu POST đến API để tạo bài đăng mới
response = requests.post("http://127.0.0.1:8000/removeBG_act?bg_color=255", data=data)

# In kết quả trả về từ API
# print(response.json())
print(response.json()['path_img_input'])