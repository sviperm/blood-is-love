from django.http import HttpResponse
from django.shortcuts import redirect, render
from analyzer.forms import ImageForm
from analyzer.models import Image
from django.conf import settings
from . import services

from keras import backend as K


def home(request):
    return redirect('analyzer:analyzer')
    # return HttpResponse('Home')


def analyzer(request):
    form = ImageForm()
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            images = []
            for i, file in enumerate(request.FILES.getlist('file')):
                # Save image locally
                image = Image.objects.create(
                    user=request.user, title='Test', file=file)
                try:
                    img_dict = image.analyze_image(form.cleaned_data)
                    img_dict['id'] = i
                    images.append(img_dict)
                    # Completely delete image
                    image.delete()
                except Exception as ex:
                    image.delete()
                    K.clear_session()
                    if settings.DEBUG:
                        raise ex
                    return render(request,
                                  template_name='error.html',
                                  context={
                                      'error_title': type(ex).__name__,
                                      'error_args': ex.args[0]
                                  })
            result = services.get_result(images)
            return render(request,
                          template_name='analyzer/analyzer.html',
                          context={'form': form,
                                   'result': result,
                                   'images': images,
                                   })
    return render(request,
                  template_name='analyzer/analyzer.html',
                  context={'form': form,
                           'images': None})


def upload(request):
    return HttpResponse('Upload')


def data(request):
    return HttpResponse('data')


def about(request):
    return HttpResponse('about')


def error(request):
    return render(request, template_name='error.html',)
