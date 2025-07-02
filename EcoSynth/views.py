from django.shortcuts import render,HttpResponse,redirect
from .import models
from django.core.mail import send_mail
from django.conf import settings
import random
def index(request):
    return render(request,'index.html')