from django.http.request import HttpRequest
from django.shortcuts import redirect


def log_required(func):
    def wrapper(*args):
        for _, arg in enumerate(args):
            if isinstance(arg, HttpRequest):
                if 'nickname' not in arg.session:
                    return redirect("home:index")
        return func(*args)
    return wrapper
