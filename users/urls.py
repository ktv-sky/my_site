from django.urls import path
from django.views.generic import RedirectView

from . import views


app_name = 'users'
urlpatterns = [
    path('', RedirectView.as_view(url='login/', permanent=True)),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
]
