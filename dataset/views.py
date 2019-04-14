from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse('test')


def upload(request):
    return render(request, template_name='dataset/upload.html')
