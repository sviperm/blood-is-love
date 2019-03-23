import base64
import os

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from pathlib import Path


def image_as_base64(image_file, format='png'):
    """
    :param `image_file` for the complete path of image.
    :param `format` is format for image, eg: `png` or `jpg`.
    """
    path = Path(image_file)
    if not os.path.isfile(path):
        return None

    encoded_string = ''
    with open(image_file, 'rb') as img_f:
        encoded_string = base64.b64encode(img_f.read()).decode('ascii')
    return f'data:image/{format};base64, {encoded_string}'

# TODO: Сделать метод для трансофрмации изображения в массив
# TODO: Сделать метод для трансофрмации массива обратно в base


class Image(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='Пользователь',
                             blank=True,
                             null=True)
    title = models.CharField(max_length=255, blank=True)
    file = models.ImageField(upload_to='photo/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Image."""

        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    def __str__(self):
        """Unicode representation of Image."""
        return self.title if self.title else str(self.id)

    def get_cover_base64(self):
        # settings.MEDIA_ROOT = '/path/to/env/projectname/media'
        return image_as_base64(Path(settings.MEDIA_ROOT) / self.file.name)


@receiver(post_delete, sender=Image)
def submission_delete(sender, instance, **kwargs):
    instance.file.delete(False)
