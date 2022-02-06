from django.urls import path
from Panel.views import Home, Image
urlpatterns = [
    path('', Home, name='Home'),
    path('image/', Image, name='Image')
]
