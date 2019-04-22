from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views import View

import time

from .forms import UploadedImageForm
from .models import UploadedImage
from .services import page_navigation


def index(request):
    return HttpResponse('test')


class UploadView(LoginRequiredMixin, View):
    login_url = '/admin/login/'
    # redirect_field_name = '/'

    def get(self, request):
        return render(request, template_name='dataset/upload.html')

    def post(self, request):
        form = UploadedImageForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.save(user=request.user, title=form.files['file'].name)
            data = {'is_valid': True,
                    'html_item': render_to_string(
                        template_name='dataset/includes/upload_item.html',
                        context={'image': image},
                        request=request)
                    }
        else:
            data = {'is_valid': False, }
        return JsonResponse(data)


class DeleteView(View):

    def post(self, request):
        pk = request.POST['pk']
        try:
            image = UploadedImage.objects.get(pk=pk)
        except UploadedImage.DoesNotExist as ex:
            data = {'success': False,
                    'html_modal_error': render_to_string(
                        template_name='dataset/includes/modal_error.html',
                        context={
                            'error_title': 'Изображения не существует',
                            'error_args': 'Запрашиваемый объект не найден', }
                    )}
        if (image.user == request.user):
            image.delete()
            data = {'success': True, }
        else:
            data = {'success': False,
                    'html_modal_error': render_to_string(
                        template_name='dataset/includes/modal_error.html',
                        context={
                            'error_title': 'Отказано в доступе',
                            'error_args': 'Нет прав на удаления изображения', }
                    )}
        return JsonResponse(data)


def dataset(request):
    return redirect('dataset:dataset_page', 1)


class DatasetView(LoginRequiredMixin, View):
    login_url = '/admin/login/'

    def get(self, request, page_num):
        image_list = UploadedImage.objects.all().order_by('id')
        paginator = Paginator(image_list, 10)
        page = paginator.get_page(page_num)
        return render(request,
                      template_name='dataset/dataset.html',
                      context={'page_num': page_num,
                               'images': page,
                               'page_nav': page_navigation(
                                   page=page,
                                   pages_nav_num=3)
                               }
                      )


def single_image(requestm, id):
    return HttpResponse(f'Single Image - {id}')
