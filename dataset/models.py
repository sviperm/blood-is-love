from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


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
        self.user = kwargs.pop('user')
        self.title = kwargs.pop('title')
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return absolute url for UploadedImage."""
        from django.urls import reverse
        return reverse('single_image', kwargs={'id': self.id, })

    def calc_margin(self):
        width = self.file.width
        height = self.file.height

        if (width > height):
            x = int(height * 173 / width)
            if (x < 155):
                return str(int((187 - x) / 2))
        return '16'


@receiver(post_delete, sender=UploadedImage)
def submission_delete(sender, instance, **kwargs):
    instance.file.delete(False)


class DataCount(models.Model):
    """Model definition for DataCount."""

    image = models.ForeignKey('UploadedImage',
                              on_delete=models.CASCADE)
    type = models.CharField(max_length=5)
    count = models.PositiveIntegerField(null=True)

    class Meta:
        """Meta definition for DataCount."""

        verbose_name = 'DataCount'
        verbose_name_plural = 'DataCounts'

    def __str__(self):
        """Unicode representation of DataCount."""
        return f'img:{self.image.id}, type: {self.type}, count: {self.count}'

    # def save(self):
    #     """Save method for DataCount."""
    #     pass

    # def get_absolute_url(self):
    #     """Return absolute url for DataCount."""
    #     return ('')

    # TODO: Define custom methods here
