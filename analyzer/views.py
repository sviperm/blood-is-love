import base64
import codecs
import urllib
from io import BytesIO

import cv2
import numpy as np
from django.http import HttpResponse
from django.shortcuts import render
from PIL import Image

from analyzer.forms import UploadFileForm

from .tests import image_to_html

# Create your views here.


def upload_file(request):
    form = UploadFileForm()
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # TODO: сохранение фотографии
            img_bytes = request.FILES['file'].file

            # # Инпут изображения
            # img = Image.open(
            #     'C:\\Users\\sviperm\\Documents\\blood-of-vlad\\analyzer\\test-img-2.png')
            # # Конвертация изображения в массив
            # img = np.asarray(img)
            # # Вся магия тут
            # img = Image.fromarray(img)
            # # Конвертация массива в изображение
            # img_bytes = BytesIO()
            # img.save(img_bytes, format='PNG')
            base64_data = codecs.encode(img_bytes.getvalue(), 'base64')
            image_src = codecs.decode(base64_data, 'ascii')
            # # Аутпут изображения
            return render(request,
                          template_name='analyzer/upload.html',
                          context={'form': form,
                                   'image_src': image_src,
                                   'file_name': form.files['file'].name})
    return render(request,
                  template_name='analyzer/upload.html',
                  context={'form': form})
