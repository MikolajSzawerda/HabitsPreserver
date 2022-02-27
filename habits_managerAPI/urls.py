from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Index.as_view()),
    path('levels/', views.FulfillmentLevels.as_view()),
    path('habits/', views.Habits.as_view({'get':'list', 'post':'create'}), name='habits'),
    path('habit/<int:pk>', views.Habits.as_view({'get':'retrieve', 'put': 'update', 'delete': 'destroy'}), name='habit'),
    path('actions/', views.HabitActions.as_view({'get':'list', 'post':'create'}), name='actions'),
    path('actions/<int:pk>', views.HabitActions.as_view({'get':'retrieve', 'put': 'update', 'delete': 'destroy'}), name='action'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
