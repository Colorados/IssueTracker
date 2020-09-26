from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import login_view, logout_view, RegisterView

app_name = 'accounts'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('create/', RegisterView.as_view(), name='create')
]