from django.urls import path
from . import views

app_name = 'datosaccion'

urlpatterns = [
    path('', views.home, name='home'),
]
