import cv2

from functools import partial

import UI.hinhanh as hinhanh  # python -m PyQt5.uic.pyuic -x UI/untitled.ui -o UI/hinhanh.py -x
from PyQt5 import QtGui, QtWidgets

import sys

# mở ảnh và lưu ảnh (ImageQt: hỗ trợ lấy hình ảnh từ label và luu)
from PIL import Image, ImageQt

# object path image
import OBJ_img
obj_img = OBJ_img.OBJ_img()  #đối tượng img để luân chuyển path hình ảnh chính
obj_img_reset = OBJ_img.OBJ_img()  # đối tượng hỗ trợ reset ảnh

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = hinhanh.Ui_MainWindow()
ui.setupUi(MainWindow)

from tkinter import filedialog as fd
def fun_ShowopenDialog():
    filename = fd.askopenfilename()  # hiển thị một hộp thoại mở tệp
    print("đã mở: " + filename)
    if(filename != ''):
        # first set enabled for all
        ui.pushButton_reset.setEnabled(True)
        ui.pushButtonsave.setEnabled(True)
        ui.groupBox_5.setEnabled(True)
        ui.groupBox_7.setEnabled(True)
        ui.pushButtonsave.setEnabled(True)
        obj_img.setimg(filename)
        obj_img_reset.setimg(filename)

        image_check = cv2.imread(filename)
    ui.label.setPixmap(QtGui.QPixmap(filename))
    ui.label_3.setPixmap(QtGui.QPixmap(filename))
    ui.label.setScaledContents(True)

def fun_ShowSaveDialog():
    files = [('Image jpg', '*.jpg'),
             ('Image Files', '*.png')]
    filename = fd.asksaveasfilename(filetypes = files, defaultextension = files)
    print("Đã lưu vào" + filename)
    # lấy hình ảnh từ label và luu
    img = ImageQt.fromqpixmap(ui.label_3.pixmap())
    if(filename!=''):
        img.save(filename)

#
# import threading
# def subfun_show_loading():
#     ui.progressBar.show()
# def subfun_hide_loading():
#     ui.progressBar.hide()
#
# def fun_color(red, blue, green):
#     t1 = threading.Thread(target=subfun_show_loading)
#     t2 = threading.Thread(target=subfun_color(red, blue, green))
#     t3 = threading.Thread(target=subfun_hide_loading)
#     t1.start()
#     t1.join()
#     t2.start()
#     t2.join()
#     t3.start()
from tkinter import messagebox
# lấy path ảnh từ object, load ảnh và xử lý màu,
def fun_color(red, blue, green):
    try:
        img = Image.open(obj_img.getimg())
        pixels = img.load()
        img_new = Image.new(img.mode, img.size)
        pixels_new = img_new.load()
        for i in range(img_new.size[0]):
            for j in range(img_new.size[1]):
                r, g, b = pixels[i, j]
                _r = r + red
                _b = b + blue
                _g = g + green
                pixels_new[i, j] = (_r, _g, _b, 255)
        # lấy tên để lưu ảnh vào chỗ tạm - lấy tên ảnh không lấy đuôi (5 dòng dưới)
        split = obj_img.getimg().split('/')
        len_split = len(split)
        # print(str(len_split))
        name_path = split[len_split - 1]
        name_path_not_ex = name_path[0:(len(name_path) - 4)]   # lấy tên, không lấy phần mở rộng
        print(name_path_not_ex)

        # lưu ảnh với tên mới và đuôi mới và path mới
        path_save_basic = './assets/img_result_filter/'
        path_save_full = path_save_basic + name_path_not_ex
        img_new.save(path_save_full + "_color" + ".jpg")
        print("Đã hoàn thành !")

        # hiển thị ảnh đã lọc lên giao diện
        ui.label_3.setPixmap(QtGui.QPixmap(path_save_full + "_color" + ".jpg"))
        # hỗ trợ lưu độ màu bên object_img lưu ào obj_img chính luôn
        # lưu path của ảnh vừa xuwr lý xong để có thể sửa màu với ảnh vừa sửa màu đó tiếp tục)
        obj_img.setimg(path_save_full + "_color" + ".jpg")
    except:
        print("đang bị lỗi ở fun_color")
        messagebox.showinfo("Thông báo", "Lỗi! Có thể do ảnh không tương thích")

import glob
import os
def delete_All_File():
    files = glob.glob('./assets/img_result_filter/*.jpg')
    for f in files:
        try:
            os.unlink(f)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))

def fun_Reset():
    delete_All_File()
    ui.label_3.setPixmap(QtGui.QPixmap(obj_img_reset.getimg()))
    obj_img.setimg(obj_img_reset.getimg())
    ui.groupBox_5.setEnabled(True)

import requests
def subfun_xulyBG(url_API):
    try:
        # B1: tạo data để gửi lên API với key: value
        data = {
            # "path_input": "C:\\Users\\Tin Ngo\\Desktop\\imageTest\\red-car.png"
            "path_input": str(obj_img.getimg())
        }
        # B2: gửi data lên API với phương thức POST và nhận phản hồi lưu vào biến response
        response = requests.post(url_API, data=data)
        print(response.json())  # api trả về path img gửi lên, và img đã xử lý

        # b3: lưu img kết quả vào 1 thư mục phụ
        response = requests.get(response.json()['path_img_result'])
        with open("./assets/img_result_BG/image.jpg", "wb") as f:
            f.write(response.content)
        # B4: hiển thị img lên Qlabel từ path ảnh trong thư mục phụ vừa lưu
        ui.label_3.setPixmap(QtGui.QPixmap("./assets/img_result_BG/image.jpg"))
    except:
        print("đang bị lỗi ở fun_BG")
        messagebox.showinfo("Thông báo", "Lỗi! Có thể do API bị lỗi, hãy thử lại nhé")

def fun_removeBG():
    # lấy text của combobox xem người dùng chọn nền trắng hay đen hay trong suốt
    value = ui.comboBox.currentText()   # lấy text hiện tại của combobox
    # print(value)
    if str(value) == 'white':
        subfun_xulyBG("http://127.0.0.1:8000/removeBG_act?bg_color=255")
    if str(value) == 'black':
        subfun_xulyBG("http://127.0.0.1:8000/removeBG_act?bg_color=0")
    if str(value) == 'transparent':
        subfun_xulyBG("http://127.0.0.1:8000/removeBG_act?bg_color=999")
    else:
        print("Giá trị combobox không phù hợp => "+value)
def fun_blurBG():
    subfun_xulyBG("http://127.0.0.1:8000/blurBG_act")
def fun_grayBG():
    subfun_xulyBG("http://127.0.0.1:8000/grayBG_act")
def fun_changeBG():
    try:
        img_background = fd.askopenfilename()
        if img_background != '':
            print("Đã nhận ảnh subject: "+str(obj_img.getimg()))
            print("Đã nhận ảnh background: "+str(img_background))
            data = {
                "path_input_subject": str(obj_img.getimg()),
                "path_input_bg": str(img_background)
            }
            # B2: gửi data lên API với phương thức POST và nhận phản hồi lưu vào biến response
            response = requests.post("http://127.0.0.1:8000/changeBG_act", data=data)
            print(response.json())  # api trả về path img gửi lên, và img đã xử lý
        #
        # b3: lưu img kết quả vào 1 thư mục phụ
        response = requests.get(response.json()['path_img_result'])
        with open("./assets/img_result_BG/image.jpg", "wb") as f:
            f.write(response.content)
        # B4: hiển thị img lên Qlabel từ path ảnh trong thư mục phụ vừa lưu
        ui.label_3.setPixmap(QtGui.QPixmap("./assets/img_result_BG/image.jpg"))
    except:
        print("đang bị lỗi ở fun_changeBG")
        messagebox.showinfo("Thông báo", "Lỗi! Có thể do API bị lỗi, thử lại sau nhé")

def giaodien():
    #main window
    MainWindow.setStyleSheet("QMainWindow{\n"
                                 "    border-image: url(./assets/img/background.png);\n"
                                 "}\n"
                                 "\n"
                                 "")
    #set disabled and enabled(open image)
    ui.pushButton.setEnabled(True)
    ui.pushButton_reset.setEnabled(False)
    ui.pushButtonsave.setEnabled(False)
    ui.groupBox_5.setEnabled(False)
    ui.groupBox_7.setEnabled(False)
    ui.pushButtonsave.setEnabled(False)

    # progress
    # ui.progressBar.setMinimum(0)  # cho thanh progressBar mặc định chạy toàn bộ thanh
    # ui.progressBar.setMaximum(0)  # cho thanh progressBar mặc định chạy toàn bộ thanh
    ui.progressBar.hide()  # tạm thời ẩn thanh progressBar

    #Groupbox chữ màu trắng
    ui.groupBox_7.setStyleSheet("QGroupBox {color : white; }")
    ui.groupBox_5.setStyleSheet("QGroupBox {color : white; }")

    #hiển thị ảnh đầu tiên
    ui.label.setPixmap(QtGui.QPixmap("./assets/img/placeholder_img.png"))
    ui.label_3.setPixmap(QtGui.QPixmap("./assets/img/placeholder_img.png"))

    #QLabel
    ui.label_4.setStyleSheet("QLabel {color : white; }")
    ui.label_2.setStyleSheet("QLabel {color : white; }")
    ui.label_5.setStyleSheet("QLabel {color : white; }")
    ui.label_6.setStyleSheet("QLabel {color : white; }")
    ui.label_7.setStyleSheet("QLabel {color : white; }")

    # comboBox ("drop down") chức năng xóa nền
    ui.comboBox.addItem("white")
    ui.comboBox.addItem("black")
    ui.comboBox.addItem("transparent")

    #QPushButton
    ui.pushButton.setStyleSheet("QPushButton { color: white; background-color: green; border-radius: 10px; font-weight: bold;}")
    ui.pushButtonsave.setStyleSheet("QPushButton { color: white; background-color: green; border-radius: 10px; font-weight: bold;}")
    ui.pushButton_reset.setStyleSheet("QPushButton { color: white; background-color: gray; border-radius: 10px; font-weight: bold;}")
    ui.pushButtonsave.setStyleSheet("QPushButton { color: white; background-color: green; border-radius: 10px; font-weight: bold;}")

def mainMenu():
    # xử lý các sự kiện click button
    ui.pushButton.clicked.connect(fun_ShowopenDialog)

    # Chức năng: tăng - giảm màu
    ui.pushButton_4.clicked.connect(partial(fun_color, 20, 0, 0))  # tăng đỏ
    ui.pushButton_3.clicked.connect(partial(fun_color, -20, 0, 0))  # giảm đỏ
    ui.pushButton_7.clicked.connect(partial(fun_color, 0, 20, 0))  # tăng blue
    ui.pushButton_6.clicked.connect(partial(fun_color, 0, -20, 0))  # giảm blue
    ui.pushButton_8.clicked.connect(partial(fun_color, 0, 0, 20))  # tăng green
    ui.pushButton_5.clicked.connect(partial(fun_color, 0, 0, -20))  # giảm green

    # chức năng reset
    ui.pushButton_reset.clicked.connect(fun_Reset)
    # chức năng save ảnh
    ui.pushButtonsave.clicked.connect(fun_ShowSaveDialog)

    # Chức năng xóa nền ảnh
    ui.pushButton_removeBG.clicked.connect(fun_removeBG)
    # chức năng làm mờ nền ảnh
    ui.pushButton_blurBG.clicked.connect(fun_blurBG)
    # chức năng làm xám nền ảnh
    ui.pushButton_grayBG.clicked.connect(fun_grayBG)
    # chức năng thay đổi nền ảnh
    ui.pushButton_changeBG.clicked.connect(fun_changeBG)

    MainWindow.show()


if __name__ == '__main__':
    giaodien()
    mainMenu()
    sys.exit(app.exec_())  # để cho cửa sổ không bị tắt liền khi mới chạy được