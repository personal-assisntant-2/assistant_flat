from django.db import models
from django.conf import settings


class UploadedFiles(models.Model):
    name = models.TextField(verbose_name="Name of file")
    extension = models.CharField(max_length=10)
    file = models.BinaryField(
        # max_length=None
    )
    size = models.CharField(max_length=10)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="files"
    )

