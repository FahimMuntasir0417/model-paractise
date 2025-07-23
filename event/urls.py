from django.urls import path
from . import views

from .views import signup_view, login_view, dashboard_view

urlpatterns = [
    path('create-category/', views.create_category, name='create_category'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('activate/<int:uid>/<str:token>/', views.activate, name='activate'),
]
    # Example: path('', views.home, name='home'),
