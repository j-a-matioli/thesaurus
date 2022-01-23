from django.conf import settings
from django.shortcuts import render
from django.contrib import messages

def home(request):
    msgs =  messages.get_messages(request)
    for msg in msgs:
        msgs.used = True
    return render(request, 'core/index.html')
