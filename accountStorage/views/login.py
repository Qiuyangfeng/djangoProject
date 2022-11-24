from accountStorage.untils.check_code import check_code
from io import BytesIO
from accountStorage.untils.forms import LoginForm, RegisterFrom
from accountStorage.models import AdminUser
from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


def login (request):
    if request.method == "GET":
        if request.session.get('info'):
            return redirect("accountStorage:account_list")
        form = LoginForm()
        register_admin = RegisterFrom()
        return render(request, 'accountStorage/login.html', {"form": form, 'register': register_admin})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        # 去数据库校验账号密码
        user_input_code = form.cleaned_data.pop('code')
        image_show_code = request.session.get('image_code', "")
        print(form.cleaned_data)
        if image_show_code.upper() != user_input_code.upper():
            form.add_error("code", "验证码错误")
            return render(request, 'accountStorage/login.html', {"form": form})
        admin_project = AdminUser.objects.filter(**form.cleaned_data).first()
        print(admin_project)
        if not admin_project:
            form.add_error("password", "用户名或密码错误")
            return render(request, 'accountStorage/login.html', {"form": form})
        # 用户名密码正确 网站生成随机字符串 存到用户cookie中，写入session中
        request.session["info"] = {'id': admin_project.id, 'username': admin_project.username}
        request.session.set_expiry(60 * 60 * 24 * 7)
        return redirect("accountStorage:account_list")
    return render(request, 'accountStorage/login.html', {"form": form})


def logout (request):
    """注销"""
    request.session.flush()
    return redirect("accountStorage:login")


def image_code (request):
    """生成图片验证码"""
    # 调用pillow函数 生产图片
    img, code_string = check_code()
    # 写入到自己的session中,60秒过期
    request.session['image_code'] = code_string
    request.session.set_expiry(60)
    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())


@csrf_exempt
def register (request):
    register_data = {}
    form = RegisterFrom(data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data)
        confirm_password = form.cleaned_data.pop('confirm_password')
        password = form.cleaned_data['register_password']
        if confirm_password != password:
            form.add_error("confirm_password", "密码不一致")
            return JsonResponse({'status': False, 'error': form.errors})
        register_data['username'] = form.cleaned_data['register_username']
        register_data['password'] = form.cleaned_data['register_password']
        AdminUser.objects.create(**register_data)
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})
