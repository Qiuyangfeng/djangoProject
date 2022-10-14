"""
自定义分页组件，使用这个分页组件需要做如下几件事
在视图函数中
from app01.untils.pagination import Pagination
def pretty_list (request):
    # 1.根据自己的情况去筛选数据库数据
    queryset = models.PrettyNum.objects.all()
    # 实例化分页对象
    page_object = Pagination(request, queryset)
    context = {
        "queryset": page_object.page_queryset,
        "page_string": page_object.html()
    }
    return render(request, "pretty_list.html", context)
在html页面中
       {% for i in queryset %}
       {{ i.xxx }}
       {% endfor %}

        <ul class="pagination" >
            {{ page_string }}
        </ul>
"""
from django.utils.safestring import mark_safe
from copy import deepcopy

class Pagination(object):
    def __init__(self, request, queryset, page_size=10, page_param="page", plus = 3):
        """
        :param request: 请求的对象
        :param queryset: 符合条件的数据库数据
        :param page_size: 每页显示多少条数据
        :param page_param: 在url中传递的获取分页的参数，例如：/pretty/list/？page=12
        :param plus: 显示当前页 前或后几页
        """
        query_dict = deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict
        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size
        self.page_param = page_param
        self.start = (page - 1) * page_size
        self.end = page * page_size
        self.page_queryset = queryset[self.start:self.end]
        total_count = queryset.count()
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count
        self.plus = plus

    def html(self):
        # 首页
        page_str_list = []
        self.query_dict.setlist(self.page_param, [1])
        page_str_list.append('<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))
        # 计算出显示当前页的前5页 后五页

        start_page = self.page - self.plus
        self.query_dict.setlist(self.page_param, [self.page - 1])
        last_page = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        if start_page < 1:
            start_page = 1
        if self.page == 1:
            last_page = ''
        end_page = self.page + self.plus
        self.query_dict.setlist(self.page_param, [self.page + 1])
        next_page = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        if end_page > self.total_page_count:
            end_page = self.total_page_count
        if self.page == self.total_page_count:
            next_page = ''
        # 上一页
        page_str_list.append(last_page)
        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)
        page_str_list.append(next_page)
        #
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        page_str_list.append('<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode()))
        jump_str = """ <form method="get">
                         <div class="input-group">
                           <span class="input-group-btn">
                             <input type="text" name="page"
                               style="position: relative;float: left;display: inline-block;width: 80px;border-radius: 0;"
                               required="required" class="form-control" placeholder="页码">
                             <button style="position: relative;float: left;display: inline-block;width: 80px;border-radius: 0;"
                            class="btn btn-default" type="submit">跳转</button>
                           </span>
                          </div>
                       </form>"""
        page_str_list.append(jump_str)
        page_string = mark_safe("".join(page_str_list))
        return page_string
