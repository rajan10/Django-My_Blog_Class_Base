
from django.urls import path, include
from .views import RegistrationView,loginView, logoutView

urlpatterns =[
    path('register/', RegistrationView.as_view(), name="register"),
    path('login/', loginView.as_view(), name="login"),
    path('logout/', logoutView, name="logout"),
]