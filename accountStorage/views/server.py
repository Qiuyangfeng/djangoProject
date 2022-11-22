from django.shortcuts import render, redirect
from django.http import JsonResponse
from accountStorage.untils.forms import ServerModelForm
from django.core.paginator import Paginator
from accountStorage.models import ServerInfo
from django.views.decorators.csrf import csrf_exempt
import pandas as pd

def server_list(request):
    """服务器列表"""
    # for i in range(20):
    #     server = {
    #         "hostname": "测试服务器{}".format(i),
    #         "ipaddress": "172.16.1.{}".format(i),
    #         "platform": "1",
    #         "protocols": "1",
    #         "port": "22",
    #         "note": "测试备注{}".format(i)
    #     }
    #     ServerInfo.objects.create(**server)
    #     ServerInfo.objects.filter(username="test{}".format(i)).delete()
    data = {}
    search_data = request.GET.get('search', "")
    if search_data:
        data["username__contains"] = search_data
    form = ServerModelForm()
    data_list = ServerInfo.objects.filter(**data).order_by("-hostname")
    paginator = Paginator(data_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    keys = ServerInfo._meta.fields
    keys_list = [keys[i].name for i in range(len(keys))]
    context = {
        "title": "服务器列表",
        "search_data": search_data,
        "key_list": keys_list,
        "data_list": data_list,
        "page_obj": page_obj,
        "form": form,
        "excel_url": "/media/excel/server.xlsx",
    }
    return render(request, 'accountStorage/server.html', context)


@csrf_exempt
def server_add(request):
    """添加服务器(ajax请求)"""
    form = ServerModelForm(data=request.POST)
    if form.is_valid():
        # 随机生成订单号
        # form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))
        # form.instance.admin_id = request.session['info']['id']
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


def server_detail(request):
    """获取服务器详情"""
    hostname = request.GET.get("hostname")
    row_dict = ServerInfo.objects.filter(hostname=hostname).values("hostname", "ipaddress", "platform", "protocols", "port",
                                                        "note").first()
    if not row_dict:
        return JsonResponse({"status": False, 'error': "数据不存在"})
    result = {"status": True, 'data': row_dict}
    return JsonResponse(result)

@csrf_exempt
def server_edit (request):
    """账号编辑"""
    hostname = request.GET.get("hostname")
    row_object = ServerInfo.objects.filter(hostname=hostname).first()
    if not row_object:
        return JsonResponse({"status": False, 'tips': "数据不存在"})
    form = ServerModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, 'error': form.errors})

def server_delete (request):
    """服务器删除"""
    hostname = request.GET.get('hostname')
    exists = ServerInfo.objects.filter(hostname=hostname).exists()
    if not exists:
        return JsonResponse({"status": False, 'error': "删除失败，数据不存在"})
    ServerInfo.objects.filter(hostname=hostname).delete()
    return JsonResponse({"status": True, 'msg': "删除成功"})

@csrf_exempt
def upload_ajax_excel (request):
    """ajax上传excel，读取数据写入数据库"""
    if request.method == 'POST':
        file_object = request.FILES.get('files')
        df = pd.read_excel(file_object, keep_default_na=False)
        print(df)
        for i in df.index.values:
            df_dict = df.loc[i, ["hostname", "ipaddress", "platform", "protocols", "port", "note"]].to_dict()
            print(df_dict)
            ServerInfo.objects.create(**df_dict)
        return redirect("/account/server/")
    return JsonResponse({'status': False, 'error': 'excel异常'})
