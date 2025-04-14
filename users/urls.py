from django.urls import path
from users.views import UserCreationView

urlpatterns = [
    path('signup/', UserCreationView.as_view(), name='signup'),
]