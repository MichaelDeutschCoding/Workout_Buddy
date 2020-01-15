from django.urls import path
from accounts import views


app_name = 'accounts'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/edit', views.edit_profile, name='edit-profile'),
    path('profile/', views.view_profile, name='my-profile'),
    path('profile/<int:user_id>', views.view_profile, name='profile'),
]
