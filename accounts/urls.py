from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns=[
    path('register/',views.RegitserView.as_view(),name='register'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout/',views.LogoutUserView.as_view(),name='logout'),
    path('profile/',views.ProfileView.as_view(),name='profile'),
    path('profile/update/',views.ProfileUpdateView.as_view(),name='profile_update'),
    path('refresh_token/',TokenRefreshView.as_view(),name='refresh_token'),
]
