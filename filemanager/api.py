from .models import UploadedFiles
from django.core.exceptions import ValidationError


def create_uploaded_file(name: str, extension: str, file: bytes, user, size: int) -> UploadedFiles:
    uploaded_file = UploadedFiles.objects.create(
            name=name,
            extension=extension,
            file=file,
            user=user,
            size=size
        )


def normalize(text: str) -> str:
    """
    if the text contains Cyrillic letters, then the function replaces them with the Latin.
    :return: updated text.
    """
    cyrillic = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    latin = ['a', 'b', 'v', 'g', 'd', 'e', 'ye', 'zh', 'z', 'i', 'y', 'k', 'l', 'm', 'n', 'o',
             'p', 'r', 's', 't', 'u', 'f', 'kh', 'ts', 'ch', 'sh', 'shch', '', 'y', '', 'e', 'yu', 'ya']

    translit_dict = dict()
    for c, l in zip(cyrillic, latin):
        translit_dict[ord(c)] = l
        translit_dict[ord(c.upper())] = l.upper()
    translated_text = text.translate(translit_dict)

    return translated_text


def file_size(value):
    """
    Checks the file size, if more than 2 MiB (2.097152 Mbyte) - raises a ValidationError.
    :param value: InMemoryUploadedFile.
    """
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 2 MiB.')
