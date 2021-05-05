from django.urls import path, include
from auth_users.views import RegisterView, UserEditView, LoginView, LogoutView

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth_register/', RegisterView.as_view(), name='signup'),
    path('auth_user/', UserEditView.as_view(), name='user_edit'),
    path('auth_login/', LoginView.as_view(), name='login'),
    path('auth_logout/', LogoutView.as_view(), name='logout'),
]
