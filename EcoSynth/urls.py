from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('uregister/', views.uregister, name='uregister'),
    path('ulogin/', views.ulogin, name='ulogin'),
    path('ulist/', views.ulist, name='ulist'),
    path('udashboard/', views.udashboard, name='udashboard'),
    path('feedback/', views.feedback, name='feedback'),
    path('ueditprofile/', views.ueditprofile, name='ueditprofile'),
    path('uprofile/', views.uprofile, name='uprofile'),
    path('pickup/', views.pickup_page, name='pickup'),
    path('repair/', views.repair_request_view, name='repair'),
    path('sell/', views.sell_product_view, name='sell'),
    path('buy/', views.buy_view, name='buy'),
    path('sell/delete/<int:id>/', views.delete_product_view, name='delete_product'),
    path('sell/edit/<int:id>/', views.edit_product_view, name='edit_product'),

]