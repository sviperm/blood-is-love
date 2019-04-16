import time
from collections import namedtuple
from os.path import normcase

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views import View

from .forms import UploadedImageForm
from .models import UploadedImage


def index(request):
    return HttpResponse('test')


class UploadView(View):
    def get(self, request):
        return render(request, template_name='dataset/upload.html')

    def post(self, request):
        time.sleep(1)
        form = UploadedImageForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            # TODO: Сделать одной строчкой
            image = form.save(commit=False)
            image.title = form.files['file'].name
            image.save()
            data = {'is_valid': True,
                    'html_item': render_to_string(
                        template_name='dataset/item_container.html',
                        context={'image': image},
                        request=request)
                    }
        else:
            data = {'is_valid': False, }
        return JsonResponse(data)


class DeleteView(View):

    def post(self, request):
        pk = request.POST['pk']
        image = UploadedImage.objects.get(pk=pk)
        # TODO: add user vaildation
        image.delete()
        data = {'success': True, }
        return JsonResponse(data)


def single_image(request):
    return HttpResponse('Single Image')
