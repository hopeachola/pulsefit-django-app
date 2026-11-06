from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # <-- Fixed line (removed get_admin_urls)
    path('fitness/', include('myapp.urls')), 
]
