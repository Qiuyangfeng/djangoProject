import os
import uuid
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .forms import FileUploadForm, FileUploadModelForm
from .models import File

def file_list(request):
    """文件列表"""
    files = File.objects.all().order_by('-id')
    return render(request, 'fileStorage/file_list.html', {'files': files})


def handle_uploaded_file(file):
    ext = file.name.split(',')[-1]
    file_name = "{}.{}".format(uuid.uuid4().hex[:10], ext)
    file_path = os.path.join('media', 'files', file_name)
    absolute_file_path = os.path.join('media', 'files', file_name)
    directory = os.path.dirname(absolute_file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(absolute_file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return file_path


def file_upload(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            annotation = form.cleaned_data.get("annotation")
            raw_file = form.cleaned_data.get('file')
            new_file = File()
            new_file.file = handle_uploaded_file(raw_file)
            new_file.name = name
            new_file.annotation = annotation
            new_file.save()
            return redirect("/file/")
    else:
        form = FileUploadForm()
    return render(request, 'fileStorage/upload_form.html', {'form': form, 'heading': 'Upload files with Regular Form'})


def model_form_upload(request):
    if request.method == "POST":
        form = FileUploadModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # 一句话足以
            return redirect("/file/")
    else:
        form = FileUploadModelForm()

    return render(request, 'fileStorage/upload_form.html',
                  {'form': form, 'heading': 'Upload files with ModelForm'}
                  )
