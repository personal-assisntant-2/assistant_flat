import mimetypes

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages

from .forms import UploadFileForm
from .models import UploadedFiles
from .api import create_uploaded_file, normalize
from .settings import FORMATS


@login_required
def file_manager_view(request):
    """
    Responsible for uploading a file, displaying uploaded, sorting files into categories.
    """

    user = request.user

    # Upload the file and write to the database
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            handle_uploaded_file(request.FILES['file'], user)
            messages.add_message(request, messages.INFO, 'File was uploaded successfully!')
            return redirect(reverse('file_manager:file'))

        else:
            messages.add_message(request, messages.ERROR, form.errors['file'])
            return render(request, 'file_manager/file.html', {'form': form})

    # Displays a file upload form and a list of uploaded files
    form = UploadFileForm()
    selected_category = request.GET.get('category_field')
    list_files = generates_list_of_files_by_category(selected_category, user)

    return render(request, 'file_manager/file.html', {
        'form': form,
        'list_files': list_files,
        'categories': FORMATS,
        'selected_category': selected_category
    })


@login_required
def file_download_view(request, file_id):
    """
    Responsible for downloading a file, whose id = file_id.
    """
    file = get_object_or_404(UploadedFiles, pk=file_id)

    # Formation of an HTTP response
    response = HttpResponse(file.file)
    file_type = mimetypes.guess_type(file.name)

    if None in file_type:
        file_type = 'application/octet-stream'

    response['Content-Type'] = file_type
    response['Content-Length'] = str(file.size)
    response['Content-Disposition'] = "attachment; filename=" + normalize(file.name)

    return response


@login_required
def file_delete_view(request, file_id):
    file = get_object_or_404(UploadedFiles, pk=file_id)
    file.delete()
    return redirect(reverse('file_manager:file'))


def generates_list_of_files_by_category(selected_category: str, user):
    """
    Generates list of files by category.
    """
    # Displays a list by SOME category
    if selected_category:
        if selected_category == 'Others':
            list_files = UploadedFiles.objects.filter(user=user).exclude(extension__in=join_exist_extensions())
        elif selected_category in FORMATS:
            list_files = UploadedFiles.objects.filter(user=user, extension__in=FORMATS[selected_category])
        # if the selected category does not exist
        else:
            list_files = []

    # Displays list by ALL categories
    else:
        list_files = UploadedFiles.objects.filter(user=user)

    return list_files


def join_exist_extensions() -> list:
    """
    Forms a list of existing extensions
    """
    exist_extensions = []
    for extensions in FORMATS.values():
        exist_extensions += extensions

    return exist_extensions


def handle_uploaded_file(f, user):
    """
    Reading and writing file in database.
    :param f: InMemoryUploadedFile.
    :param user: User
    """
    file = b''
    # Reading file
    for chunk in f.chunks():
        file += chunk

    name: str = f.name
    extension: str = f.name.split('.')[-1]
    size: int = f.size

    # Writing file
    with transaction.atomic():
        create_uploaded_file(name, extension, file, user, size)

