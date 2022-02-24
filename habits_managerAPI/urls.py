from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view()),
    path('levels/', views.FulfillmentLevels.as_view()),
    path('habits/', views.Habits.as_view({'get':'list', 'post':'create'}), name='habits'),
    path('habits/<int:pk>', views.Habits.as_view({'get':'retrieve'}), name='habit'),
]
