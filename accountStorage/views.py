import os
import uuid

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .forms import FileUploadForm, FileUploadModelForm, UserModelForm
from .models import AccountPassword
from .models import File


def account_list(request):
    for i in range(20):
        account = {
            "name": "测试账号{}".format(i),
            "username": "test{}".format(i),
            "password": "123456".format(i),
            "note": "测试备注{}".format(i)
        }
        # AccountPassword.objects.create(**account)
    # AccountPassword.objects.filter(username="test{}.format(i)").delete()
    data = {}
    search_data = request.GET.get('search', "")
    if search_data:
        data["username__contains"] = search_data
    form = UserModelForm()
    data_list = AccountPassword.objects.filter(**data)
    paginator = Paginator(data_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    keys = AccountPassword._meta.fields
    keys_list = [keys[i].name for i in range(len(keys))]
    context = {
        "title": "账号列表",
        "search_data": search_data,
        "key_list": keys_list,
        "data_list": data_list,
        "page_obj": page_obj,
        "form": form
    }
    return render(request, 'account.html', context)


@csrf_exempt
def account_add(request):
    """添加用户 (ajax请求)"""
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # 随机生成订单号
        # form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))
        # form.instance.admin_id = request.session['info']['id']
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


def account_detail(request):
    """获取账号详情"""
    uid = request.GET.get("uid")
    row_dict = AccountPassword.objects.filter(id=uid).values("name", "username", "password", "note").first()
    if not row_dict:
        return JsonResponse({"status": False, 'error': "数据不存在"})
    result = {"status": True, 'data': row_dict}
    return JsonResponse(result)


@csrf_exempt
def account_edit(request):
    """账号编辑"""
    uid = request.GET.get("uid")
    row_object = AccountPassword.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status": False, 'tips': "数据不存在"})
    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, 'error': form.errors})


def account_delete(request):
    """账号删除"""
    uid = request.GET.get('uid')
    exists = AccountPassword.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"status": False, 'error': "删除失败，数据不存在"})
    AccountPassword.objects.filter(id=uid).delete()
    return JsonResponse({"status": True, 'msg': "删除成功"})


def file_list(request):
    """文件列表"""
    files = File.objects.all().order_by('-id')
    return render(request, 'file_list.html', {'files': files})


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
            upload_method = form.cleaned_data.get("upload_method")
            raw_file = form.cleaned_data.get('file')
            new_file = File()
            new_file.file = handle_uploaded_file(raw_file)
            new_file.upload_method = upload_method
            new_file.save()
            return redirect("/account/file/")
    else:
        form = FileUploadForm()
    return render(request, 'upload_form.html', {'form': form, 'heading': 'Upload files with Regular Form'})


def model_form_upload(request):
    if request.method == "POST":
        form = FileUploadModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # 一句话足以
            return redirect("/account/file/")
    else:
        form = FileUploadModelForm()

    return render(request, 'upload_form.html',
                  {'form': form, 'heading': 'Upload files with ModelForm'}
                  )

def upload_excel(request):
    """上传excel，读取数据写入数据库"""
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
    else:
        form = FileUploadForm()
    return render(request, 'upload_excel.html', {'form': form, 'heading': 'Upload files with Regular Form'})
