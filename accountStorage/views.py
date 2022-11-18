import pandas as pd
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from io import BytesIO
from .forms import UserModelForm, LoginForm
from .models import AccountPassword,AdminUser

def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'accountStorage/login.html', {"form": form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        #去数据库校验账号密码
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
        return redirect("/account/")
    return render(request, 'accountStorage/login.html')
def logout(request):
    """注销"""
    request.session.clear()
    return redirect("/account/login/")

def check_code (width=120, height=30, char_length=5, font_file='Monaco.ttf', font_size=28):
    code = []
    img = Image.new(mode='RGB', size=(width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img, mode='RGB')

    def rndChar ():
        """
        生成随机字母
        :return:
        """
        return chr(random.randint(65, 90))

    def rndColor ():
        """
        生成随机颜色
        :return:
        """
        return (random.randint(0, 255), random.randint(10, 255), random.randint(64, 255))

    # 写文字
    font = ImageFont.truetype(font_file, font_size)
    for i in range(char_length):
        char = rndChar()
        code.append(char)
        h = random.randint(0, 4)
        draw.text([i * width / char_length, h], char, font=font, fill=rndColor())

    # 写干扰点
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())

    # 写干扰圆圈
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=rndColor())

    # 画干扰线
    for i in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)

        draw.line((x1, y1, x2, y2), fill=rndColor())

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img, ''.join(code)

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

def account_list (request):
    """用户列表"""
    # for i in range(20):
    #     account = {
    #         "name": "测试账号{}".format(i),
    #         "username": "test{}".format(i),
    #         "password": "123456".format(i),
    #         "note": "测试备注{}".format(i)
    #     }
    #     AccountPassword.objects.create(**account)
    #     AccountPassword.objects.filter(username="test{}".format(i)).delete()
    data = {}
    search_data = request.GET.get('search', "")
    if search_data:
        data["username__contains"] = search_data
    form = UserModelForm()
    data_list = AccountPassword.objects.filter(**data).order_by("-id")
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
        "form": form,
        "excel_url": "/media/excel/account.xlsx",
    }
    return render(request, 'accountStorage/account.html', context)


@csrf_exempt
def account_add (request):
    """添加用户 (ajax请求)"""
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # 随机生成订单号
        # form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))
        # form.instance.admin_id = request.session['info']['id']
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


def account_detail (request):
    """获取账号详情"""
    uid = request.GET.get("uid")
    row_dict = AccountPassword.objects.filter(id=uid).values("name", "username", "password", "note").first()
    if not row_dict:
        return JsonResponse({"status": False, 'error': "数据不存在"})
    result = {"status": True, 'data': row_dict}
    return JsonResponse(result)



@csrf_exempt
def account_edit (request):
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

@csrf_exempt
def account_delete (request):
    """账号删除"""
    uid = request.GET.get('uid')
    exists = AccountPassword.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"status": False, 'error': "删除失败，数据不存在"})
    AccountPassword.objects.filter(id=uid).delete()
    return JsonResponse({"status": True, 'msg': "删除成功"})

@csrf_exempt
def upload_excel (request):
    """上传excel，读取数据写入数据库"""
    if request.method == 'POST':
        raw_file = request.FILES.get('file')
        print(raw_file)
        df = pd.read_excel(raw_file)
        print(df)
        df.fillna("", inplace=True)
        print(df.index.name)
        for i in df.index.values:
            df_dict = df.loc[i, ["name", "username", "password", "note"]].to_dict()
            print(df_dict)
            AccountPassword.objects.create(**df_dict)
        return redirect("/account/")
    return render(request, 'accountStorage/upload_excel.html')


@csrf_exempt
def upload_ajax_excel (request):
    """ajax上传excel，读取数据写入数据库"""
    if request.method == 'POST':
        file_object = request.FILES.get('files')
        df = pd.read_excel(file_object, keep_default_na=False)
        print(df)
        for i in df.index.values:
            df_dict = df.loc[i, ["name", "username", "password", "note"]].to_dict()
            print(df_dict)
            AccountPassword.objects.create(**df_dict)
        return redirect("/account/")
    return render(request, 'accountStorage/ajax_upload.html')
