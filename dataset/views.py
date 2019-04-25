from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Sum
from django.db.models.aggregates import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views import View

from .forms import UploadedImageForm
from .models import DataCount, UploadedImage
from .services import page_navigation


def index(request):
    return HttpResponse('test')


class UploadView(LoginRequiredMixin, View):
    login_url = '/admin/login/'

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


class DatasetView(LoginRequiredMixin, View):
    login_url = '/admin/login/'

    def get(self, request):
        total_count = UploadedImage.objects.all().count()
        neut_count = DataCount.objects.filter(
            type='neut').aggregate(Sum('count'))['count__sum']
        eosi_count = DataCount.objects.filter(
            type='eosi').aggregate(Sum('count'))['count__sum']
        baso_count = DataCount.objects.filter(
            type='baso').aggregate(Sum('count'))['count__sum']
        mono_count = DataCount.objects.filter(
            type='mono').aggregate(Sum('count'))['count__sum']
        lymph_count = DataCount.objects.filter(
            type='lymph').aggregate(Sum('count'))['count__sum']
        checked = DataCount.objects.values('image').distinct().count()
        print(checked)
        return render(request,
                      template_name='dataset/dataset.html',
                      context={'total_count': total_count,
                               'checked': checked,
                               'unchecked': total_count - checked,
                               'neut_count': neut_count,
                               'eosi_count': eosi_count,
                               'baso_count': baso_count,
                               'mono_count': mono_count,
                               'lymph_count': lymph_count,
                               })


class PieChartView(View):
    def get(self, request):
        response = {'Нейтрофилы': 1,
                    'Эозинофилы': 2,
                    'Моноциты': 1,
                    'Лимфоциты': 1,
                    'Базофилы': 2,
                    }
        return JsonResponse(response)


class DatasetPagesView(LoginRequiredMixin, View):
    login_url = '/admin/login/'

    def get(self, request, type, page_num):
        if type == 'all':
            image_list = UploadedImage.objects.all().order_by('id')
        paginator = Paginator(image_list, 10)
        page = paginator.get_page(page_num)
        return render(request,
                      template_name='dataset/dataset_pages.html',
                      context={'page_num': page_num,
                               'type': type,
                               'images': page,
                               'page_nav': page_navigation(
                                   page=page,
                                   pages_nav_num=5)
                               }
                      )


def single_image(request, id):
    image = get_object_or_404(UploadedImage, pk=id)
    image_list = UploadedImage.objects.all().order_by('id')
    for i, img in enumerate(image_list):
        if (id == img.id):
            next = ''
            previous = ''
            if (i > 0):
                previous = image_list[i-1].id
            if (i < len(image_list) - 1):
                next = image_list[i+1].id
            break
    values = [DataCount.objects.filter(image=image, type='neut').aggregate(Sum('count')),
              DataCount.objects.filter(
                  image=image, type='eosi').aggregate(Sum('count')),
              DataCount.objects.filter(
                  image=image, type='baso').aggregate(Sum('count')),
              DataCount.objects.filter(
                  image=image, type='mono').aggregate(Sum('count')),
              DataCount.objects.filter(image=image, type='lymph').aggregate(Sum('count')), ]
    print(values)
    stats = [
        {
            'id': 'neut',
            'name': 'Нейтрофилы',
            'color': 'red',
            'value': values[0]['count__sum'],
        },
        {
            'id': 'eosi',
            'name': 'Эозинофилы',
            'color': 'blue',
            'value': values[1]['count__sum'],
        },
        {
            'id': 'baso',
            'name': 'Базофилы',
            'color': 'yellow',
            'value': values[2]['count__sum'],
        },
        {
            'id': 'mono',
            'name': 'Моноциты',
            'color': 'green',
            'value': values[3]['count__sum'],
        },
        {
            'id': 'lymph',
            'name': 'Лимфоциты',
            'color': 'violet',
            'value': values[4]['count__sum'],
        },
    ]
    context = {'image': image,
               'stats': stats,
               'next': next,
               'previous': previous,
               }
    return render(request,
                  template_name='dataset/single_image.html',
                  context=context)


class UpdateCountView(View):
    def post(self, request):
        req = request.POST
        image = UploadedImage.objects.get(pk=req['image_id'])
        if req['count'] == '0':
            data = DataCount.objects.get(
                image=image, type=req['type']).delete()
        else:
            data = DataCount.objects.update_or_create(
                image=image,
                type=req['type'],
                defaults={'count': req['count']})
        response = {'success': True}
        return JsonResponse(response)
