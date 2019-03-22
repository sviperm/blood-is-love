from django.db import models
from django.contrib.auth.models import User


class Image(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='Пользователь',
                             blank=True,
                             null=True)
    title = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='photo/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
