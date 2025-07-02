from django.shortcuts import render,HttpResponse,redirect
from .import models
from django.core.mail import send_mail
from django.conf import settings
import random
def index(request):
    return render(request,'index.html')

# views.py

from django.shortcuts import render, redirect
from .models import uregistration


def uregister(request):
    if request.method == 'POST':
        name = request.POST['name']
        age = request.POST['age']
        phone = request.POST['phone']
        address = request.POST['address']
        profile_pic = request.FILES['profile_pic']

        uregistration.objects.create(
            name=name,
            age=age,
            phone=phone,
            address=address,
            profile_pic=profile_pic
        )
        return redirect('uregister')

    return render(request, 'uregister.html')

