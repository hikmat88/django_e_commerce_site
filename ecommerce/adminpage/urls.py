from django.urls import path
from .views import *

urlpatterns=[
    path('dashboard/',admin_dashboard),
    path('order/',user_order),
]