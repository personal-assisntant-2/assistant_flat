from django.db import models
from django.conf import settings

from .settings import FORMATS


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

    @property
    def category(self):
        """
        File property, depending on the extension, sets the category according to the FORMATS dictionary.
        """
        category = None
        for name_category, extensions in FORMATS.items():

            # if self.extension in list extensions with key name_category,the category name is assigned.
            if self.extension in extensions:
                category = name_category

        # If self.extension is not in the list of extensions with the name_category key,
        # the category name 'Others' is assigned.
        if category is None:
            category = 'Others'

        return category
