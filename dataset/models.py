from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.urls import reverse


class UploadedImage(models.Model):
    """Model definition for UploadedImage."""
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='Пользователь',
                             blank=True,
                             null=True)
    title = models.TextField()
    file = models.ImageField(upload_to='uploaded/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for UploadedImage."""
        verbose_name = 'UploadedImage'
        verbose_name_plural = 'UploadedImages'

    def __str__(self):
        """Unicode representation of UploadedImage."""
        return f'{self.id} - {self.title}'

    def save(self, *args, **kwargs):
        try:
            self.user = kwargs.pop('user')
        except Exception as e:
            pass

        try:
            self.title = kwargs.pop('title')
        except Exception as e:
            pass
        super(UploadedImage, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """Return absolute url for UploadedImage."""
        return reverse('dataset:single_image', kwargs={'type': 'all', 'id': self.id})

    def calc_margin(self):
        """Calculate margin on y axis when upload image"""
        width = self.file.width
        height = self.file.height

        if (width > height):
            x = int(height * 173 / width)
            if (x < 155):
                return str(int((187 - x) / 2))
        return '16'

    def has_previous_next(self, type):
        if type == 'all':
            image_list = UploadedImage.objects.all().order_by('id')
        elif type == 'checked':
            checked_list = DataCount.objects.all().values_list('image', flat=True).distinct()
            image_list = UploadedImage.objects.filter(id__in=checked_list)
        elif type == 'unchecked':
            total_list = UploadedImage.objects.all().order_by(
                'id').values_list('id', flat=True)
            checked_list = DataCount.objects.all().values_list('image', flat=True).distinct()
            unchecked_list = [x for x in total_list if x not in checked_list]
            image_list = UploadedImage.objects.filter(id__in=unchecked_list)
        elif type in ['neut', 'eosi', 'baso', 'mono', 'lymph']:
            query_list = DataCount.objects.filter(
                type=type).values_list('image', flat=True).distinct()
            image_list = UploadedImage.objects.filter(id__in=query_list)

        next_image = ''
        previous_image = ''
        for i, image in enumerate(image_list):
            if (self.id == image.id):
                if (i > 0):
                    previous_image = image_list[i - 1]
                if (i < len(image_list) - 1):
                    next_image = image_list[i + 1]
                break
        return next_image, previous_image


@receiver(post_delete, sender=UploadedImage)
def submission_delete(sender, instance, **kwargs):
    instance.file.delete(False)


class DataCount(models.Model):
    """Model definition for DataCount."""

    image = models.ForeignKey('UploadedImage', on_delete=models.CASCADE)
    type = models.CharField(max_length=5)
    count = models.PositiveIntegerField(null=True)

    class Meta:
        """Meta definition for DataCount."""

        verbose_name = 'DataCount'
        verbose_name_plural = 'DataCounts'

    def __str__(self):
        """Unicode representation of DataCount."""
        return f'img:{self.image.id}, type: {self.type}, count: {self.count}'
