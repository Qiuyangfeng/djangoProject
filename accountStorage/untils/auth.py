from django.shortcuts import redirect
from functools import wraps


# session认证装饰器
def login_check(func):
    @wraps(func)
    def wrapper(request):
        if not request.session.get('info', None):
            return redirect("accountStorage:login")
        else:
            return func(request)

    return wrapper
