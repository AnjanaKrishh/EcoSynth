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

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import uregistration, pmreg, rmreg

def ulogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check user table
        user = uregistration.objects.filter(email=email, password=password).first()
        # Inside user login success block
        if user:
            request.session['email'] = email
            request.session['user_id'] = user.id   # ✅ Store user_id too
            request.session['role'] = 'user'
            return redirect('udashboard')


        # Check pickupman table
        pickup = pmreg.objects.filter(email=email, password=password).first()
        if pickup:
            request.session['email'] = email     # ✅ store in session
            request.session['role'] = 'pickupman'
            return redirect('pmhome')

        # Check repairman table
        repair = rmreg.objects.filter(email=email, password=password).first()
        if repair:
            request.session['email'] = email
            request.session['role'] = 'repairman'
            return redirect('rmhome')

        messages.error(request, 'Invalid email or password.')  # shown if none matched

    return render(request, 'login.html')
def ulist(request):
    users = uregistration.objects.all()
    return render(request, 'ulist.html', {'users': users})

def udashboard(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('ulogin')

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

from .models import PickupRequest, uregistration
from django.utils import timezone

def pickup_page(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('ulogin')

    user = uregistration.objects.get(id=user_id)

    if request.method == 'POST':
        waste_types_selected = request.POST.getlist('waste_type')  # Get multiple selections
        address = request.POST.get('address')

        # Save as comma-separated waste types
        combined_waste_types = ", ".join(waste_types_selected)

        PickupRequest.objects.create(
            user=user,
            waste_type=combined_waste_types,
            address=address,
            requested_at=timezone.now()
        )
        return redirect('pickup')

    waste_types = ['Plastic', 'Paper', 'Metal', 'Glass', 'Electronic', 'Battery', 'Clothes', 'Steel', 'Others']
    history = PickupRequest.objects.filter(user=user).order_by('-requested_at')

    return render(request, 'pickup_page.html', {
        'waste_types': waste_types,
        'pickup_history': history,
        'user': user
    })
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


def pmregister(request):
    if request.method=='POST':
        name=request.POST.get('name')
        age=request.POST.get('age')
        email=request.POST.get('email')
        password=request.POST.get('password')
        image=request.FILES.get('image')
        if models.pmreg.objects.filter(email=email).exists():
            alert="<script>alert('email is already exist'); window.location.href='/pmregister/';</script>;"
            return HttpResponse(alert)
        else:
            user=models.pmreg(name=name,age=age,email=email,password=password,image=image)
            user.save()
            return redirect('pmlogin')
    else:   
         return render(request, 'pmregister.html')  


def pmlogin(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        try:
            user=models.pmreg.objects.get(email=email)
            if user.password==password:
                request.session['email']=email
                return redirect('pmhome')
            else:
                alert="<script>alert('invalid user'); window.location.href='/pmlogin/';</script>;"
                return HttpResponse(alert)
        except models.pmreg.DoesNotExist:
               alert="<script>alert('user not found'); window.location.href='/pmlogin/';</script>;"
               return HttpResponse(alert)          
    else:
        return render(request,'pmlogin.html')
def pmhome(request):
    email = request.session.get('email')
    if not email:
        return redirect('ulogin')  # FIXED name here

    try:
        pickupman = pmreg.objects.get(email=email)
    except pmreg.DoesNotExist:
        return redirect('ulogin')  # FIXED name here

    assigned_requests = PickupRequest.objects.filter(assigned_to=pickupman)

    return render(request, 'pmhome.html', {
        'pickupman': pickupman,
        'assigned_requests': assigned_requests
    })

def rmregister(request):
    if request.method=='POST':
        name=request.POST.get('name')
        age=request.POST.get('age')
        email=request.POST.get('email')
        password=request.POST.get('password')
        image=request.FILES.get('image')
        if models.rmreg.objects.filter(email=email).exists():
            alert="<script>alert('email is already exist'); window.location.href='/rmregister/';</script>;"
            return HttpResponse(alert)
        else:
            user=models.rmreg(name=name,age=age,email=email,password=password,image=image)
            user.save()
            return redirect('rmlogin')
    else:   
         return render(request, 'rmregister.html')  
     
     
def rmlogin(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        try:
            user=models.rmreg.objects.get(email=email)
            if user.password==password:
                request.session['email']=email
                return redirect('pmhome')
            else:
                alert="<script>alert('invalid user'); window.location.href='/rmlogin/';</script>;"
                return HttpResponse(alert)
        except models.rmreg.DoesNotExist:
               alert="<script>alert('user not found'); window.location.href='/rmlogin/';</script>;"
               return HttpResponse(alert)          
    else:
        return render(request,'rmlogin.html')

def rmhome(request):
    return render(request,'rmhome.html')   



def adminlogin(request):
    if request.method == 'POST':
        uname = request.POST.get('username')  # corrected key
        upassword = request.POST.get('password')  # corrected key
        auname = "ADMIN"
        apassword = "admin"
        if auname == uname and apassword == upassword:
            return redirect('adminhome')
        else:
            return redirect('adminlogin')
    else:
        return render(request, 'adminlogin.html')
    
def adminhome(request):
    return render(request,'adminhome.html')

def addproductlist(request):
    products = models.product.objects.all()
    return render(request,'addproductlist.html',{'products':products})

def addproduct(request):
    if request.method == 'POST':
        pname = request.POST.get('product_name')
        pdescription = request.POST.get('product_description')
        pprice = request.POST.get('product_price')
        # pcategory = request.POST.get('product_category')
        pimage = request.FILES.get('product_image')

        product = models.product(
            name=pname,
            description=pdescription,
            price=pprice,
            # category=pcategory,
            image=pimage
        )
        product.save()
        return redirect('addproductlist')
    else:
        return render(request, 'addproduct.html')
    
def editproduct(request, product_id):
    product = models.product.objects.get(id=product_id)
    if request.method == 'POST':
        product.name = request.POST.get('product_name')
        product.description = request.POST.get('product_description')
        product.price = request.POST.get('product_price')
        product.image = request.FILES.get('product_image', product.image)
        product.save()
        return redirect('addproductlist')
    return render(request, 'editproduct.html', {'product': product})

def deleteproduct(request, product_id):
    product = models.product.objects.get(id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('addproductlist')
    return render(request, 'deleteproduct.html', {'product': product})

from .models import product
def product_list(request):
    products = product.objects.all()  # Fetch all products added by admin
    return render(request, 'product_list.html', {'products': products})

from .models import pmreg, rmreg

def add_workers_option(request):
    return render(request, 'add_workers_option.html')

from django.contrib import messages  # ✅ Add this
def add_pickupman(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        password = request.POST.get('password')
        image = request.FILES.get('image')

        # Check if email already exists
        if pmreg.objects.filter(email=email).exists():
            messages.error(request, "This email is already used.")
            return redirect('add_pickupman')

        # Save to database
        pmreg.objects.create(
            name=name,
            age=age,
            email=email,
            phone=phone,
            address=address,
            password=password,
            image=image
        )
        messages.success(request, "Pickupman added successfully!")
        return redirect('worker_list')  # Ensure this URL name exists

    return render(request, 'add_pickupman.html')

def add_repairman(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        password = request.POST.get('password')
        image = request.FILES.get('image')

        rmreg.objects.create(
            name=name,
            age=age,
            email=email,
            phone=phone,
            address=address,
            password=password,
            image=image
        )
        return redirect('worker_list')  # or any page you want to go after adding

    return render(request, 'add_repairman.html')

from .models import pmreg, rmreg,DeliveryRequest  # Import both models

def worker_list(request):
    pickupmen = pmreg.objects.all()
    repairmen = rmreg.objects.all()
    deliveries = DeliveryRequest.objects.select_related('user', 'assigned_to').all()

    return render(request, 'worker_list.html', {
        'pickupmen': pickupmen,
        'repairmen': repairmen,
        'deliveries': deliveries
    })

from .models import PickupRequest, pmreg
def pickup_requests_view(request):
    pickup_requests = PickupRequest.objects.all().order_by('-requested_at')
    pickupmen = pmreg.objects.all()

    return render(request, 'pickuprequests.html', {
        'pickup_requests': pickup_requests,
        'pickupmen': pickupmen
    })


def assign_pickupman(request, request_id):
    if request.method == 'POST':
        pickupman_id = request.POST.get('pickupman_id')
        pickup_request = get_object_or_404(PickupRequest, id=request_id)
        pickupman = get_object_or_404(pmreg, id=pickupman_id)

        pickup_request.assigned_to = pickupman
        pickup_request.status = 'Assigned'
        pickup_request.save()
        return redirect('pickuprequests')

from django.shortcuts import get_object_or_404, redirect
from .models import PickupRequest

def pickup_done(request, request_id):
    if request.method == 'POST':
        pickup = get_object_or_404(PickupRequest, id=request_id)
        pickup.status = 'Completed'
        pickup.save()
    return redirect('pmhome')



from django.shortcuts import get_object_or_404, redirect
from .models import PickupRequest

def add_points(request, pickup_id):
    if request.method == 'POST':
        # ✅ Correct way to get multiple checkbox values
        selected_categories = request.POST.getlist('waste_category')

        # Points per category
        points_mapping = {
            'Plastic': 8,
            'Metal': 10,
            'Paper and Cardboard': 5,
            'Electronic': 25,
            'Glass': 12,
            'Others': 6,
        }

        # Calculate total points
        total_points = sum([points_mapping.get(cat, 0) for cat in selected_categories])

        # Get the pickup object
        pickup = get_object_or_404(PickupRequest, id=pickup_id)

        # Add points to the user
        user = pickup.user
        user.points += total_points
        user.save()

        # Optionally prevent re-adding points
        pickup.points_assigned = True
        pickup.save()

        return redirect('pmhome')
def add_delivery(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        password = request.POST.get('password')
        image = request.FILES.get('image')

        rmreg.objects.create(
            name=name,
            age=age,
            email=email,
            phone=phone,
            address=address,
            password=password,
            image=image
        )
        return redirect('worker_list')  # or any page you want to go after adding

    return render(request, 'add_delivery.html')


from .models import product, Cart, uregistration
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

def add_to_cart(request, product_id):
    if 'email' not in request.session:
        messages.error(request, "You must be logged in to add to cart.")
        return redirect('ulogin')  # adjust to your login route

    user_email = request.session.get('email')
    user = get_object_or_404(uregistration, email=user_email)

    product_obj = get_object_or_404(product, id=product_id)

    # Check if already in cart
    cart_item, created = Cart.objects.get_or_create(user=user, product=product_obj)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{product_obj.name} added to cart!")
    return redirect('product_list')


def view_cart(request):
    if 'email' not in request.session:
        return redirect('ulogin')

    user_email = request.session.get('email')
    user = get_object_or_404(uregistration, email=user_email)

    cart_items = Cart.objects.filter(user=user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from .models import Cart, uregistration

def checkout(request):
    if 'email' not in request.session:
        return redirect('ulogin')

    user_email = request.session['email']
    user = get_object_or_404(uregistration, email=user_email)

    # Update cart items status
    cart_items = Cart.objects.filter(user=user, status='In Cart')
    if cart_items.exists():
        cart_items.update(status='Ordered')
        messages.success(request, "Order placed successfully!")
    else:
        messages.warning(request, "No items in your cart to checkout.")

    return redirect('view_cart')


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
def services(request):
     return render(request,'services.html')

def about(request):
    return render(request,'about.html')
def contact(request):
    return render(request,'contact.html')


def map(request):
    return render(request, 'map.html')  # You'll create this template

def blogs(request):
    return render(request, 'blogs.html')  # You'll create this template

from django.shortcuts import redirect

def logout(request):
    request.session.flush()  # Clears all session data
    return redirect('index')  # Redirect to home page (change if needed)

def add_deliveryman(request):
    # You can add your logic here
    return render(request, 'add_deliveryman.html')

def forgot_password(request):
    return render(request, 'forgot_password.html')
