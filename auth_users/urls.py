from django.urls import path, include
from auth_users.views import RegisterView, UserView

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth_register/', RegisterView.as_view(), name='signup'),
    path('auth_user/', UserView.as_view(), name='auth'),
]
