from django.urls import path
from users.views import ThrottleTokenObtainPairView, ThrottleTokenRefreshView
from users.views import UserCreate

urlpatterns = [
    path('', UserCreate.as_view(), name='user_create'),
    path('token/', ThrottleTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', ThrottleTokenRefreshView.as_view(), name='token_refresh'),
]