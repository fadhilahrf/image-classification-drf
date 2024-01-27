from django.urls import path, include
from .views import hello_world

app_name = 'main_app'

urlpatterns = [
    path('home/', hello_world, name='home'),
]