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
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        password = request.POST['password']
        profile_pic = request.FILES['profile_pic']

        uregistration.objects.create(
            name=name,
            age=age,
            email=email,
            phone=phone,
            address=address,
            password=password,
            profile_pic=profile_pic
        )
        return redirect('ulogin')

    return render(request, 'uregister.html')

def ulogin(request):
    if request.method == 'POST':
        email = request.POST['email'].strip().lower()
        password = request.POST['password'].strip()

        print(f"Entered login: {email} / {password}")
        for u in uregistration.objects.all():
            print(f"User in DB: {u.email} / {u.password}")

        try:
            user = uregistration.objects.get(email=email, password=password)
            request.session['user_id'] = user.id
            return redirect('udashboard')
        except uregistration.DoesNotExist:
            return render(request, 'ulogin.html', {'error': 'Invalid email or password'})

    return render(request, 'ulogin.html')

def ulist(request):
    users = uregistration.objects.all()
    return render(request, 'ulist.html', {'users': users})

def udashboard(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('ulogin')  # force login

    user = uregistration.objects.get(id=user_id)
    return render(request, 'udashboard.html', {'user': user})

from .models import Feedback, uregistration 
def feedback(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('ulogin')
    
    user = uregistration.objects.get(id=user_id)

    if request.method == 'POST':
        message = request.POST['message'].strip()
        rating = request.POST.get('rating', 0)

        if message:
            Feedback.objects.create(user=user, message=message, rating=rating)
            return render(request, 'feedback.html', {'success': 'Thank you for your feedback!'})
        else:
            return render(request, 'feedback.html', {'error': 'Please enter your feedback.'})

    return render(request, 'feedback.html')

def ueditprofile(request):
    user_id = request.session.get('user_id')
    user = uregistration.objects.get(id=user_id)

    if request.method == 'POST':
        user.name = request.POST['name']
        user.email = request.POST['email']
        user.phone = request.POST['phone']
        user.address = request.POST['address']
        if 'profile_pic' in request.FILES:
            user.profile_pic = request.FILES['profile_pic']
        user.save()
        return redirect('udashboard')

    return render(request, 'ueditprofile.html', {'user': user})


def uprofile(request):
    user_id = request.session.get('user_id')
    user = uregistration.objects.get(id=user_id)
    return render(request, 'uprofile.html', {'user': user})

from django.shortcuts import render, redirect
from .models import PickupRequest, uregistration
from django.utils import timezone

def pickup_page(request):
    if request.method == 'POST':
        waste_type = request.POST.get('waste_type')
        address = request.POST.get('address')

        # Assume user is already logged in and stored in session
        user_id = request.session.get('user_id')
        user = uregistration.objects.get(id=user_id)

        PickupRequest.objects.create(
            user=user,
            waste_type=waste_type,
            address=address,
            requested_at=timezone.now()
        )
        return redirect('pickup')  # redirect to the same page

    user_id = request.session.get('user_id')
    if user_id:
        user = uregistration.objects.get(id=user_id)
        history = PickupRequest.objects.filter(user=user).order_by('-requested_at')
    else:
        history = []

    waste_types = ['Plastic', 'Paper', 'Metal', 'Glass', 'Electronic', 'Battery', 'Clothes', 'Steel', 'Others']
    return render(request, 'pickup_page.html', {'waste_types': waste_types, 'pickup_history': history})

# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import RepairRequest, uregistration
from django.shortcuts import render, redirect
from .models import RepairRequest, uregistration

def repair_request_view(request):
    # Use session-based user if not using Django's auth User model
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('ulogin')  # redirect to login if session missing

    user = uregistration.objects.get(id=user_id)

    device_types = ['Laptop', 'Smartphone', 'Tablet', 'Monitor', 'Printer', 'Router', 'TV', 'Game Console']
    repair_history = RepairRequest.objects.filter(user=user).order_by('-requested_at')

    if request.method == 'POST':
        device_type = request.POST.get('device_type')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        description = request.POST.get('description')

        RepairRequest.objects.create(
            user=user,
            device_type=device_type,
            phone=phone,
            address=address,
            description=description
        )
        return redirect('repair')

    return render(request, 'repair.html', {
        'device_types': device_types,
        'repair_history': repair_history,
        'user': user,
    })


from django.shortcuts import render, redirect
from .models import SellProduct, uregistration
def sell_product_view(request):
    if request.method == 'POST':
        device_name = request.POST.get('device_name')
        image = request.FILES.get('image')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        # Use a default/test user if not logged in
        user = uregistration.objects.first()  # ⚠️ Replace with session-based logic later

        SellProduct.objects.create(
            user=user,
            device_name=device_name,
            image=image,
            phone=phone,
            address=address
        )
        return redirect('sell')

    # Default/test user for displaying form data
    user = uregistration.objects.first()  # ⚠️ Same note as above

    products = SellProduct.objects.filter(user=user).order_by('-posted_at')
    return render(request, 'sell.html', {'user': user, 'products': products})





def buy_view(request):
    products = SellProduct.objects.all().order_by('-posted_at')
    return render(request, 'buy.html', {'products': products})


from django.shortcuts import get_object_or_404

def delete_product_view(request, id):
    product = get_object_or_404(SellProduct, id=id)

    # Optional: Add this line to restrict delete to only the user who uploaded
    # if product.user != request.user.uregistration:
    #     return HttpResponseForbidden()

    product.delete()
    return redirect('sell')

from django.shortcuts import get_object_or_404, redirect, render
from .models import SellProduct

def edit_product_view(request, id):
    product = get_object_or_404(SellProduct, id=id)

    # Optional: Only allow the owner to edit
    # if product.user != request.user.uregistration:
    #     return HttpResponseForbidden()

    if request.method == 'POST':
        product.device_name = request.POST.get('device_name')
        if request.FILES.get('image'):
            product.image = request.FILES.get('image')
        product.phone = request.POST.get('phone')
        product.address = request.POST.get('address')
        product.save()
        return redirect('sell')

    return render(request, 'edit_product.html', {'product': product})
