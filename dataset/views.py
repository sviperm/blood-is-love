import time
from collections import namedtuple
from os.path import normcase

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views import View

from .forms import UploadedImageForm
from .models import UploadedImage


def index(request):
    return HttpResponse('test')


class UploadView(View):
    def get(self, request):
        return render(request, template_name='dataset/upload.html')

    def post(self, request):
        time.sleep(0.7)
        form = UploadedImageForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            # TODO: Сделать одной строчкой
            image = form.save(commit=False)
            image.title = form.files['file'].name
            image.save()
            data = {'is_valid': True,
                    'id': image.id,
                    'name': image.title,
                    'url': image.file.url,
                    'margin': image.calc_margin(), }
        else:
            data = {'is_valid': False, }
        return JsonResponse(data)

    def delete(self, request):

        return HttpResponse()


def single_image(request):
    return HttpResponse('Single Image')
