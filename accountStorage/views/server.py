from django.shortcuts import render, redirect

def server_list (request):
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