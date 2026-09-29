from django.urls import path

from accounts.views import register_custom_user_view

urlpatterns = [
    path('register/', register_custom_user_view, name="register")
]