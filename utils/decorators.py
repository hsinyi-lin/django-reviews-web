from django.shortcuts import render, redirect


def user_login_required(function):
    def wrapper(request, *args, **kw):
        if 'sessionid' not in request.COOKIES.keys():
            return redirect('/login/')
        else:
            return function(request, *args, **kw)
    return wrapper