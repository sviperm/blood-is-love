from django import forms
from django.utils.translation import gettext as _


class UploadFileForm(forms.Form):
    file = forms.ImageField(label='')
    # widget=forms.ClearableFileInput(attrs={'multiple': True}))
