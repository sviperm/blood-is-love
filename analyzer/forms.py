from django import forms
from django.utils.translation import gettext as _

from analyzer.models import Image

# class UploadFileForm(forms.Form):
#     file = forms.ImageField(label='')
#     widget = forms.ClearableFileInput(attrs={'multiple': True}))


class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ("file",)
