import os
from django.conf import settings

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def home(request):
    print('BASE_DIR :' ,settings.BASE_DIR)
    print('STATIC_URL :' ,settings.STATIC_URL)
    print('STATIC_ROOT :' ,settings.STATIC_ROOT)
    return render(request, 'core/index.html')
