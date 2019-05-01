from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Sum
from django.db.models.aggregates import Count
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View

from .forms import UploadedImageForm
from .models import DataCount, UploadedImage
from .services import page_navigation


class UploadView(LoginRequiredMixin, View):
    login_url = '/admin/login/'

    def get(self, request):
        return render(request, template_name='dataset/upload.html')

    def post(self, request):
        form = UploadedImageForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.save(user=request.user, title=form.files['file'].name)
            data = {
                'is_valid': True,
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
        try:
            image = UploadedImage.objects.get(pk=request.POST['pk'])
            next_image, previous_image = image.has_previous_next(request.POST['type'])
            if next_image:
                redirect_url = next_image.get_absolute_url()
            elif previous_image:
                redirect_url = previous_image.get_absolute_url()
            else:
                redirect_url = reverse("dataset:dataset")
            image.delete()
            data = {
                'success': True,
                'redirect_url': redirect_url,
            }
        except UploadedImage.DoesNotExist as ex:
            data = {
                'success': False,
                'html_modal_error': render_to_string(
                    template_name='dataset/includes/modal_error.html',
                    context={
                        'error_title': 'Изображения не существует',
                        'error_args': 'Запрашиваемый объект не найден',
                    }
                ),
            }
        return JsonResponse(data)


class DatasetView(LoginRequiredMixin, View):
    login_url = '/admin/login/'

    def get(self, request):
        total_images_num = UploadedImage.objects.all().count()
        checked_images_num = DataCount.objects.values('image').distinct().count()
        unchecked_images_num = total_images_num - checked_images_num

        statistics = {
            'images': {
                'total': total_images_num,
                'checked': checked_images_num,
                'unchecked': unchecked_images_num,
            },
            'cells': {
                'total': {
                    'name': 'Всего клеток',
                    'url': reverse('dataset:dataset_view', kwargs={'type': 'checked', 'page_num': 1, }),
                    'color': 'grey',
                    'count': DataCount.objects.all().aggregate(Sum('count'))['count__sum'],
                },
                'types': [],
            },
        }

        cell_labels = ['Нейтрофилы', 'Эозинофилы', 'Базофилы', 'Моноциты', 'Лимфоциты']
        cell_tags = ['neut', 'eosi', 'baso', 'mono', 'lymph']
        cell_colors = ['red', 'blue', 'yellow', 'green', 'purple']

        for i in range(len(cell_tags)):
            cell_stat = {
                'name': cell_labels[i],
                'url': reverse('dataset:dataset_view', kwargs={'type': cell_tags[i], 'page_num': 1, }),
                'color': cell_colors[i],
                'count': DataCount.objects.filter(type=cell_tags[i]).aggregate(Sum('count'))['count__sum'],
            }
            statistics['cells']['types'].append(cell_stat)

        return render(request,
                      template_name='dataset/dataset.html',
                      context={'statistics': statistics, })


class PieChartView(View):
    def get(self, request):
        labels = ['Нейтрофилы', 'Эозинофилы', 'Базофилы', 'Моноциты', 'Лимфоциты']
        cell_tags = ['neut', 'eosi', 'baso', 'mono', 'lymph']

        data = []
        for i in range(len(labels)):
            count = DataCount.objects.filter(
                type=cell_tags[i]).aggregate(Sum('count')),
            data.append(count[0]['count__sum'])

        response = {
            'labels': labels,
            'data': data,
        }
        return JsonResponse(response)


class DatasetPagesView(LoginRequiredMixin, View):
    login_url = '/admin/login/'

    def get(self, request, type, page_num):
        if type == 'all':
            image_list = UploadedImage.objects.all().order_by('id')
        elif type == 'checked':
            checked_list = DataCount.objects.all().values_list('image', flat=True).distinct()
            image_list = UploadedImage.objects.filter(id__in=checked_list)
        elif type == 'unchecked':
            total_list = UploadedImage.objects.all().order_by('id').values_list('id', flat=True)
            checked_list = DataCount.objects.all().values_list('image', flat=True).distinct()
            unchecked_list = [x for x in total_list if x not in checked_list]
            image_list = UploadedImage.objects.filter(id__in=unchecked_list)
        elif type in ['neut', 'eosi', 'baso', 'mono', 'lymph']:
            query_list = DataCount.objects.filter(type=type).values_list('image', flat=True).distinct()
            image_list = UploadedImage.objects.filter(id__in=query_list)
        else:
            raise Http404("Poll does not exist")

        paginator = Paginator(image_list, 10)
        page = paginator.get_page(page_num)
        return render(request,
                      template_name='dataset/dataset_pages.html',
                      context={
                          'page_num': page_num,
                          'type': type,
                          'images': page,
                          'page_nav': page_navigation(
                              page=page,
                              pages_nav_num=5,)
                      })


def single_image(request, type, id):
    image = get_object_or_404(UploadedImage, pk=id)
    next_image, previous_image = image.has_previous_next(type=type)
    cell_tags = ['neut', 'eosi', 'baso', 'mono', 'lymph']
    cell_labels = ['Нейтрофилы', 'Эозинофилы', 'Базофилы', 'Моноциты', 'Лимфоциты']
    cell_colors = ['red', 'blue', 'yellow', 'green', 'purple']
    stats = []

    for i in range(len(cell_tags)):
        value = DataCount.objects.filter(image=image, type=cell_tags[i]).aggregate(Sum('count')),
        value = value[0]['count__sum']
        stat = {
            'id': cell_tags[i],
            'label': cell_labels[i],
            'color': cell_colors[i],
            'value': value,
        }
        stats.append(stat)

    context = {
        'image': image,
        'stats': stats,
        'type': type,
        'previous_image': previous_image,
        'next_image': next_image,
    }
    return render(request,
                  template_name='dataset/single_image.html',
                  context=context)


class UpdateCountView(View):
    def post(self, request):
        image = UploadedImage.objects.get(pk=request.POST['image_id'])
        if request.POST['count'] == '0':
            data = DataCount.objects.get(image=image, type=request.POST['type']).delete()
        else:
            data = DataCount.objects.update_or_create(
                image=image,
                type=request.POST['type'],
                defaults={'count': request.POST['count'], }
            )
        response = {'success': True, }
        return JsonResponse(response)
