from django.http import HttpResponse
from django.urls import path, include
from django.contrib import admin

def home(request):
    return HttpResponse("OK - RAILWAY FUNCIONA")

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('auth/', include('adapters.auth_urls')),
    path('core/', include('core.urls')),
    path('payments/', include('payments.urls')),
]