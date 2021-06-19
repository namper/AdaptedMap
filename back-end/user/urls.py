from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from user.views import CreateUserView, user_logout, UserView

app_name = 'user'


urlpatterns = [
    path('register/', CreateUserView.as_view(), name='register'),
    path('api-token-auth/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', user_logout, name='logout'),
    path('details/', UserView.as_view(), name='details'),
]
