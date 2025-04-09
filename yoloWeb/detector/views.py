# detector/views.py
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from ultralytics import YOLO
import os

# 你可以選擇合適的 YOLO 模型
model = YOLO('yolov8n.pt')

def index(request):
    return render(request, 'index.html')

def upload(request):
    if request.method == 'POST' and request.FILES['image']:
        uploaded_file = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_url = fs.url(filename)

        # 偵測圖片中的物體
        results = model(filename)

        # 保存處理後的圖片
        result_image_path = os.path.join('media', 'result_' + filename)
        results.save(result_image_path)

        return render(request, 'result.html', {
            'image_url': file_url,
            'result_image': '/media/' + 'result_' + filename
        })
    return render(request, 'index.html')
