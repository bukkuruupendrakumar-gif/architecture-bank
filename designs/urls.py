from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('designs/<int:id>/', views.designs, name="designs"),
]
