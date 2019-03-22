import base64
import codecs
import urllib
from io import BytesIO

import cv2
import numpy as np
from django.http import HttpResponse
from django.shortcuts import redirect, render
from PIL import Image as pil_img

from analyzer.forms import ImageForm
from analyzer.models import Image


def home(request):
    return redirect('analyzer:analyzer')
    # return HttpResponse('Home')


def analyzer(request):
    form = ImageForm()
    if request.method == 'POST':
        user = request.user
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            for file in request.FILES.getlist('file'):
                # TODO: сделать проверку на уже имеющееся фотографии
                # Сохранение фотографий
                image = Image.objects.create(file=file)
                # # Инпут изображения
                # img = Image.open(
                #       C:\\Users\\sviperm\\Documents\\blood-of-vlad\\analyzer\\test-img-2.png')
                # # Конвертация изображения в массив
                # img = np.asarray(img)
                # # Вся магия тут
                # img = Image.fromarray(img)
                # # Конвертация массива в изображение
                # img_bytes = BytesIO()
                # img.save(img_bytes, format='PNG')
                # base64_data = codecs.encode(img_bytes.getvalue(), 'base64')
                # image_src = codecs.decode(base64_data, 'ascii')
                # # Аутпут изображения
            return render(request,
                          template_name='analyzer/analyzer.html',
                          context={'form': form,
                                   #    'image_src': image_src,
                                   #    'file_name': form.files['file'].name
                                   })
    return render(request,
                  template_name='analyzer/analyzer.html',
                  context={'input': True,
                           'form': form})


def upload(request):
    return HttpResponse('Upload')


def data(request):
    return HttpResponse('data')


def about(request):
    return HttpResponse('about')
