from django import forms
from django.utils.translation import gettext as _

from analyzer.models import Image

# class UploadFileForm(forms.Form):
#     file = forms.ImageField(label='')
#     widget = forms.ClearableFileInput(attrs={'multiple': True}))


class ImageForm(forms.ModelForm):
    # TODO: сделать форму вот такой
    # <input type="file" class="custom-file-input" name="file" accept="image/*" required="" id="id_file" multiple="">
    class Meta:
        model = Image
        fields = ("file",)
