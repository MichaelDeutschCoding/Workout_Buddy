from django.urls import path, reverse
from app import views


urlpatterns = [
    path('', views.landing, name='landing'),
    path('home/', views.home, name='home'),
    path('add-sport-profile/<sport_type>', views.add_sport_profile, name='add-sport-profile'),
    path('sport-profiles/riding/', views.RidingFilterView.as_view(), name='riding-profiles'),
    path('sport-profiles/running/', views.RunningFilterView.as_view(), name='running-profiles'),
    path('sport-profiles/workout/', views.WorkoutFilterView.as_view(), name='workout-profiles'),
    path('messages/', views.view_messages, name='messages'),
    path('messages/inbox', views.inbox, name='inbox'),
    path('messages/<int:message_id>', views.read_message, name='read-message'),
    path('messages/send', views.send_message, name='send-message'),
    path('routes/', views.RouteList.as_view(), name='all-routes'),
    path('routes/new/', views.RouteCreate.as_view(), name='add-route'),
]
