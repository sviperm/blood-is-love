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

    # def save(self):
    #     """Save method for UploadedImage."""
    #     pass

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

    def get_name(self):
        pass
        # TODO: метод визуализации в HTML


@receiver(post_delete, sender=UploadedImage)
def submission_delete(sender, instance, **kwargs):
    instance.file.delete(False)
