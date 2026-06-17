from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("🚀 RAILWAY FUNCIONANDO PERFECTO")

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('auth/', include('adapters.auth_urls')),
    path('core/', include('core.urls')),
    path('payments/', include('payments.urls')),
]