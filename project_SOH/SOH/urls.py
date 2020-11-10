from django.urls import path, include
from SOH import views

urlpatterns = [
    path('index/', views.index),

]
