from django.urls import path
from .views import LoginView, LogoutView, RateChangeView

urlpatterns = [
    path('api/login/', LoginView.as_view()),
    path('api/logout/', LogoutView.as_view()),
    path('api/rate-change/', RateChangeView.as_view()),
]