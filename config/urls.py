from django.http import HttpResponse
from django.urls import path

def home(request):
    return HttpResponse("🚀 RAILWAY FUNCIONA PERFECTO")

urlpatterns = [
    path("", home),
]