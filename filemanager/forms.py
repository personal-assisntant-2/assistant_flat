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


# CATEGORY_CHOICES = (
#     ('', ''),
#     ('audio', 'Audios'),
#     ('archive', 'Archives'),
#     ('doc', 'Documents'),
#     ('img', 'Images'),
#     ('video', 'Video'),
#     ('others', 'Others')
# )
#
#
# class CategoryForm(forms.Form):
#     category_field = forms.ChoiceField(
#         choices=CATEGORY_CHOICES,
#         required=False,
#     )

