from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view()),
    path('levels/', views.FulfillmentLevels.as_view()),
]
