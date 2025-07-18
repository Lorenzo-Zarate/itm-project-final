from django.urls import path

from . import views

app_name = 'item'

urlpatterns = [
    path('browse/', views.browse, name='browse'),
    path('<int:pk>/', views.detail, name='detail'),
]