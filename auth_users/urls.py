from django.urls import path, include
from auth_users.views import RegisterView, UserEditView, MyObtainTokenPairView, ChangePasswordView, LogoutView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('auth/update_user/<int:pk>/', UserEditView.as_view(), name='auth_user_edit'),
    path('auth/login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('auth/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', LogoutView.as_view(), name='auth_logout'),
    path('auth/change_password/<int:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),
]
