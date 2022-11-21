from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

class AuthMiddleware(MiddlewareMixin):
    """中间件"""
    def process_request(self, request):
        # 0. 排除不需要登录就能访问的页面
        if request.path_info in ['/account/login/', '/account/image/code/', '/admin/*']:
            return
        # 1读取登录信息
        info_dict = request.session.get("info")
        if info_dict:
            return
        # 2 未登录则跳转到登录页面
        return redirect('/account/login/')