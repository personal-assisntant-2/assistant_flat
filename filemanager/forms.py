from django import forms
from .api import file_size


class UploadFileForm(forms.Form):
    """
    File upload form.
    """
    file = forms.FileField(
        # up to 2 MiB
        validators=[file_size],
        label='Upload file'
    )


