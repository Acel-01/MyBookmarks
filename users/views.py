from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle
from djoser import signals
from djoser.conf import settings
from djoser.compat import get_user_email
from templated_mail.mail import BaseEmailMessage
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.models import User
from users.serializers import UserSerializer

# Create your views here.

class ConfirmationEmail(BaseEmailMessage):
    template_name = "confirmation_email.html"
    
class UserCreate(generics.CreateAPIView):
    throttle_classes = [AnonRateThrottle]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    lookup_field = settings.USER_ID_FIELD

    def get_permissions(self):
        self.permission_classes = settings.PERMISSIONS.user_create
        return super().get_permissions()

    def get_serializer_class(self):
        return settings.SERIALIZERS.user_create_password_retype
    
    def get_instance(self):
        return self.request.user
    
    def perform_create(self, serializer, *args, **kwargs):
        user = serializer.save(*args, **kwargs)
        signals.user_registered.send(
            sender=self.__class__, user=user, request=self.request
        )

        context = {"user": user}
        to = [get_user_email(user)]
        settings.EMAIL.confirmation(self.request, context).send(to)

class ThrottleTokenObtainPairView(TokenObtainPairView):
    throttle_classes = [AnonRateThrottle]

class ThrottleTokenRefreshView(TokenRefreshView):
    throttle_classes = [AnonRateThrottle]