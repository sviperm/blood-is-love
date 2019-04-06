import base64
import codecs
import urllib
from io import BytesIO

import cv2
import numpy as np
from keras import backend as K
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
            images = []
            for i, file in enumerate(request.FILES.getlist('file')):
                # TODO: сделать проверку на уже имеющееся фотографии
                # Save image locally
                image = Image.objects.create(
                    user=request.user, title='Test', file=file)
                try:
                    img_dict = image.analyze_image(form.cleaned_data)
                    img_dict['id'] = i
                    images.append(img_dict)
                    error = ''
                except Exception as e:
                    K.clear_session()
                    error = e
                # Completely delete image
                image.delete()
            return render(request,
                          template_name='analyzer/analyzer.html',
                          context={'error': error,
                                   'form': form,
                                   'images': images,
                                   })
    return render(request,
                  template_name='analyzer/analyzer.html',
                  context={'error': None,
                           'form': form,
                           'images': None})


def upload(request):
    return HttpResponse('Upload')


def data(request):
    return HttpResponse('data')


def about(request):
    return HttpResponse('about')


def error(request):
    return render(request, template_name='error.html',)
