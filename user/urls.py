from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('api/auth/signup/',views.signup),
    path('api/auth/login/',views.MyTokenObtainPairView.as_view()),
    path('api/auth/reset/password/',views.forgot_password),
    path('api/auth/reset/password/<token>/',views.reset_password)
]
