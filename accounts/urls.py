from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('register/', views.registration_view, name = 'register'),
    path('login/', views.login_view, name = 'login'),
    path('logout/', LogoutView.as_view(), name = 'logout')
]