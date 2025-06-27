from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('confirmations.urls')),  # All confirmation-related endpoints under /api/
]