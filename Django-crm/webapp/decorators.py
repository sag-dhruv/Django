from django.shortcuts import redirect, render
from django.http import HttpResponse


def user_is_authenticated(view_func):
    '''if user is authenticated then redirect to home page for signup & login page
    if enter manually url like register/ or login/'''
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper_func


def allowed_users(roles=[]):
    '''This decoratoer allows customer users to hide products,customers & order page
    so that he/she doesn't create,update or delete order and see products & customers'''
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in roles:
                return view_func(request, *args, **kwargs)
            return HttpResponse('You are not allowed to view this page')
        return wrapper_func
    return decorator


def admin_only(view_func):
    '''It allows admin user to see home page & customer to see user page'''
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'customer':
            return redirect('user-page')
        if group == 'admin':
            return view_func(request, *args, **kwargs)

    return wrapper_func
