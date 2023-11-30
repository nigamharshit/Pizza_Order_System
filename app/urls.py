from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('order/', views.generate_order, name='generate_order'),
    path('get_order_status/<int:order_id>/', views.get_order_status, name='get_order_status'),
]