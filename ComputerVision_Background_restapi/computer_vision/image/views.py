from django.shortcuts import render

# Create your views here.

import rembg
import uuid
from PIL import Image

from torchvision import models
from PIL import Image
import matplotlib.pyplot as plt
import torch
import numpy as np
import cv2
import os
import os.path

# Apply the transformations needed
import torchvision.transforms as T

# các hàm để xóa nền ảnh
from .ModuleBG import removeBG as module_removeBG
from .ModuleBG import changeBG
from .ModuleBG import blurBG as module_blurBG
from .ModuleBG import gray_scaleBG as module_gray
from .ObjectBG import object as object_BG

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers

# đường dẫn để lưu ảnh
path_save_removeBG = "home/static/image/removeBG/"
path_show_removeBG = "../static/image/removeBG/"
path_get_common = "home/static/image/preProcessing/"
#  chức năng thay đổi nền ảnh
path_anhnen_changeBG = "home/static/image/changeBG/imageBG/"
path_ketqua_changeBG = "home/static/image/changeBG/result/"
path_hienthiHTML_changeBG = "../static/image/changeBG/result/"
path_tailen_common = "home/static/image/preProcessing/" # là ảnh chủ thể - sẽ xóa bỏ nền để bỏ vào nền mới 
# làm mờ nền ảnh
path_ketqua_blurBG = "home/static/image/blurBG/"
path_hienthiHTML_blurBG = "../static/image/blurBG/"
# làm xám - gray nền ảnh
path_ketqua_grayBG = "home/static/image/grayBG/"
path_hienthiHTML_grayBG = "../static/image/grayBG/"


# xóa tất cả hình ảnh trong thư mục - theo đường dẫn lưu ảnh và đường dẫn lấy ảnh
def delete_all_image_infolder():
    for filename in os.listdir(path_save_removeBG):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')): # Các định dạng file ảnh cần xóa
            os.remove(os.path.join(path_save_removeBG, filename))
    # for filename in os.listdir(path_get_common):
    #     if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')): # Các định dạng file ảnh cần xóa
    #         os.remove(os.path.join(path_get_common, filename))
    for filename in os.listdir(path_anhnen_changeBG):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')): # Các định dạng file ảnh cần xóa
            os.remove(os.path.join(path_anhnen_changeBG, filename))
    for filename in os.listdir(path_ketqua_changeBG):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')): # Các định dạng file ảnh cần xóa
            os.remove(os.path.join(path_ketqua_changeBG, filename))

# hàm gọi xóa tất cả hình ảnh - gọi khi remove bg
def close_all_image(request):
    delete_all_image_infolder()
    return render(request, 'removeBG.html')


# XÓA NỀN ẢNH

# remove background
@api_view(['POST'])
def remove_background(request):
    delete_all_image_infolder()
    # nếu có nhận input type=file thì chạy web / else thì chạy api => đều trả về API
    if 'image_input' in request.FILES:   #request.method == 'POST' and 
        uploaded_image = request.FILES['image_input']
        input = Image.open(uploaded_image)
        file_name = uploaded_image.name
        
    else:   # đây là nhận path ảnh - cho các ứng dụng desktop
        # uploaded_image = r"C:\Users\Tin Ngo\Desktop\imageTest\red-car.png"
        # input = Image.open(r"C:\Users\Tin Ngo\Desktop\imageTest\red-car.png")
        # nhận dữ liệu từ rest api method post mà không dùng serializer
        uploaded_image = str(request.data.get('path_input'))
        print("Đã nhận được path " + uploaded_image)
        # print("Bực thiệt chứ:  " + request.data.get('OK_path_input'))
        input = Image.open(uploaded_image)
        # file_name = "red-car.png"
        file_name = os.path.basename(uploaded_image)

    # # ở lần click thứ 2 thì không gửi ảnh qua POST nữa mà sẽ lấy path được set vào object ở lần đầu khi click
    # elif object_BG.pathImg_removeBG.getPath() != None:
    #     # uploaded_image = r"C:\Users\Tin Ngo\Desktop\imageTest\red-car.png"
    #     # input = Image.open(r"C:\Users\Tin Ngo\Desktop\imageTest\red-car.png")
    #     # nhận dữ liệu từ rest api method post mà không dùng serializer
    #     uploaded_image = str(object_BG.pathImg_removeBG.getPath())
    #     # print("Bực thiệt chứ:  " + request.data.get('OK_path_input'))
    #     input = Image.open(uploaded_image)
    #     # file_name = "red-car.png"
    #     file_name = os.path.basename(uploaded_image)

    
    input.save("home/static/image/preProcessing/" + file_name)
    object_BG.pathImg_removeBG.setPath(path_get_common + file_name)

    if request.GET.get('bg_color') != None:
        bg_color = request.GET.get('bg_color')
        bg_color = int(bg_color)
        if bg_color != 999:  # là nếu =999 là nền trong suốt => dùng thư viện rembg
            rgb = module_removeBG.segment(module_removeBG.dlab, object_BG.pathImg_removeBG.getPath(), color_bg = bg_color, show_orig=False)
            rgb_new = (rgb * 255).astype('uint8')
            brg = cv2.cvtColor(rgb_new, cv2.COLOR_BGR2RGB)
            filename = str(uuid.uuid4()) + '.png'
            # path_image_save = path_save_removeBG + filename
            # cv2.imwrite(path_image_save, brg.astype('uint8'))
        else:
            input = Image.open(str(object_BG.pathImg_removeBG.getPath()))
            output = rembg.remove(input)
            # đặt tên ảnh random
            filename = str(uuid.uuid4()) + '.png'
            path_image_save = path_save_removeBG + filename
            output.save(path_image_save)
            return Response({"path_img_input": "http://127.0.0.1:8000/static/image/preProcessing/" + file_name,\
                     "path_img_result": "http://127.0.0.1:8000/static/image/removeBG/" + filename})
    else:
        rgb = module_removeBG.segment(module_removeBG.dlab, path_get_common + file_name, color_bg = 255, show_orig=False)

    rgb_new = (rgb * 255).astype('uint8')
    brg = cv2.cvtColor(rgb_new, cv2.COLOR_BGR2RGB)
    filename = str(uuid.uuid4()) + '.png'
    path_image_save = path_save_removeBG + filename
    cv2.imwrite(path_image_save, brg.astype('uint8'))

    return Response({"path_img_input": "http://127.0.0.1:8000/static/image/preProcessing/" + file_name,\
                     "path_img_result": "http://127.0.0.1:8000/static/image/removeBG/" + filename})



# THAY ĐỔI NỀN HÌNH ẢNH

# change background lần đầu
@api_view(['POST'])
def change_background(request):
    delete_all_image_infolder()
    
    if 'img_subject' in request.FILES:
        # lưu ảnh subject
        uploaded_image = request.FILES['img_subject']
        input = Image.open(uploaded_image)
        file_name = uploaded_image.name

    else:   # đây là nhận path ảnh - cho các ứng dụng desktop
        uploaded_image = str(request.data.get('path_input_subject'))
        print("Đã nhận được path ảnh chủ thể: " + uploaded_image)
        input = Image.open(uploaded_image)
        file_name = os.path.basename(uploaded_image)

    input.save(path_tailen_common + file_name)
    object_BG.pathImg_changeBG.setPath(path_tailen_common + file_name)

    if 'img_bg' in request.FILES:
        # lưu ảnh background
        uploaded_image_bg = request.FILES['img_bg']
        input_bg = Image.open(uploaded_image_bg)
        file_name_bg = uploaded_image_bg.name
    else:   # đây là nhận path ảnh - cho các ứng dụng desktop
        uploaded_image_bg = str(request.data.get('path_input_bg'))
        print("Đã nhận được path background: " + uploaded_image_bg)
        input_bg = Image.open(uploaded_image_bg)
        file_name_bg = os.path.basename(uploaded_image_bg)
    
    input_bg.save(path_anhnen_changeBG + file_name_bg)
    object_BG.pathImg_changeBG.setPath(path_anhnen_changeBG + file_name_bg)

    rgb = changeBG.segment(changeBG.dlab, path_tailen_common + file_name, path_anhnen_changeBG + file_name_bg, show_orig=False)

    rgb_new = (rgb * 255).astype('uint8')
    brg = cv2.cvtColor(rgb_new, cv2.COLOR_BGR2RGB)
    filename = str(uuid.uuid4()) + '.png'
    path_image_save = path_ketqua_changeBG + filename
    cv2.imwrite(path_image_save, brg.astype('uint8'))

    return Response({"path_img_input_subject": "http://127.0.0.1:8000/static/image/preProcessing/" + file_name,\
                    "path_img_input_bg": "http://127.0.0.1:8000/static/image/changeBG/imageBG/" + file_name_bg,\
                     "path_img_result": "http://127.0.0.1:8000/static/image/changeBG/result/" + filename})
  



#  LÀM MỜ NỀN HÌNH ẢNH

# làm mờ nền ảnh
@api_view(['POST'])
def blur_background(request):
    delete_all_image_infolder()
    if 'input_img_blur' in request.FILES:
        uploaded_image = request.FILES['input_img_blur']
        input = Image.open(uploaded_image)
        file_name = uploaded_image.name
    else:   # đây là nhận path ảnh - cho các ứng dụng desktop
        uploaded_image = str(request.data.get('path_input'))
        print("Đã nhận được path " + uploaded_image)
        input = Image.open(uploaded_image)
        file_name = os.path.basename(uploaded_image)

    input.save(path_tailen_common + file_name)
    object_BG.pathImg_blurBG.setPath(path_tailen_common + file_name)

    rgb = module_blurBG.segment(module_blurBG.dlab, path_tailen_common + file_name, show_orig=False)

    rgb_new = (rgb * 255).astype('uint8')
    brg = cv2.cvtColor(rgb_new, cv2.COLOR_BGR2RGB)
    filename = str(uuid.uuid4()) + '.png'
    path_image_save = path_ketqua_blurBG + filename
    cv2.imwrite(path_image_save, brg.astype('uint8'))

    return Response({"path_img_input": "http://127.0.0.1:8000/static/image/preProcessing/" + file_name,\
                     "path_img_result": "http://127.0.0.1:8000/static/image/blurBG/" + filename})






#  LÀM Gray NỀN HÌNH ẢNH

@api_view(['POST'])
def gray_background(request):
    delete_all_image_infolder()
    if 'input_img_gray' in request.FILES:
    # lưu ảnh subject
        uploaded_image = request.FILES['input_img_gray']
        input = Image.open(uploaded_image)
        file_name = uploaded_image.name
    else:   # đây là nhận path ảnh - cho các ứng dụng desktop
        uploaded_image = str(request.data.get('path_input'))
        print("Đã nhận được path " + uploaded_image)
        input = Image.open(uploaded_image)
        file_name = os.path.basename(uploaded_image)

    input.save(path_tailen_common + file_name)
    object_BG.pathImg_grayBG.setPath(path_tailen_common + file_name)

    rgb = module_gray.segment(module_gray.dlab, path_tailen_common + file_name, show_orig=False)

    rgb_new = (rgb * 255).astype('uint8')
    brg = cv2.cvtColor(rgb_new, cv2.COLOR_BGR2RGB)
    filename = str(uuid.uuid4()) + '.png'
    path_image_save = path_ketqua_grayBG + filename
    cv2.imwrite(path_image_save, brg.astype('uint8'))

    return Response({"path_img_old": "http://127.0.0.1:8000/static/image/preProcessing/" + file_name,\
                     "path_img_result": "http://127.0.0.1:8000/static/image/grayBG/" + filename})