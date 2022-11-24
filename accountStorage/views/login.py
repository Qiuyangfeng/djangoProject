from accountStorage.untils.check_code import check_code
from io import BytesIO
from accountStorage.untils.forms import LoginForm
from accountStorage.models import AdminUser
from django.shortcuts import render, redirect, HttpResponse


def login(request):
    if request.method == "GET":
        if request.session.get('info'):
            return redirect("accountStorage:account_list")
        form = LoginForm()
        return render(request, 'accountStorage/login.html', {"form": form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data)
        # 去数据库校验账号密码
        user_input_code = form.cleaned_data.pop('code')
        image_code = request.session.get('image_code', "")
        if image_code.upper() != user_input_code.upper():
            form.add_error("code", "验证码错误")
            return render(request, 'accountStorage/login.html', {"form": form})
        admin_project = AdminUser.objects.filter(**form.cleaned_data).first()
        if not admin_project:
            form.add_error("password", "用户名或密码错误")
            return render(request, 'accountStorage/login.html', {"form": form})
        # 用户名密码正确 网站生成随机字符串 存到用户cookie中，写入session中
        request.session["info"] = {'id': admin_project.id, 'username': admin_project.username}
        request.session.set_expiry(60 * 60 * 24 * 7)
        return redirect("accountStorage:account_list")
    return render(request, 'accountStorage/login.html', {"form": form})


def logout(request):
    """注销"""
    request.session.flush()
    return redirect("accountStorage:login")


def image_code(request):
    """生成图片验证码"""
    # 调用pillow函数 生产图片
    img, code_string = check_code()
    # 写入到自己的session中,60秒过期
    request.session['image_code'] = code_string
    request.session.set_expiry(60)
    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())

def register(request):
    return HttpResponse("ok")
