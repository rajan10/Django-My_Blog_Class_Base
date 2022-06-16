from django.contrib import admin
from django.urls import path, include
from .views import HomeView,CreatePostView, DetailPostView, UpdatePostView, DeletePostView

urlpatterns = [
    path('', HomeView.as_view(), name="index"),
    path('create_post', CreatePostView.as_view(), name="create_post"),
    path('detail_post/<int:pk>', DetailPostView.as_view(), name="detail_post"),
    path('update_post/<int:pk>', UpdatePostView.as_view(), name="update_post"),
    path('delete_post/<int:pk>', DeletePostView.as_view(), name="delete_post"),
]