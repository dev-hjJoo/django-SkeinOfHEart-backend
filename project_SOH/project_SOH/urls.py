from django.contrib import admin
from django.urls import path, include
from project_SOH import loads, saves

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ai/', include('SOH.urls')),
    path('load_pages', loads.load_pages),
    path('save_user', saves.save_user),
    path('save_page', saves.save_page),
]
