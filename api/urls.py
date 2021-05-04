from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import viewsets, views

router = DefaultRouter()
router.register(r'images', viewsets.ImageViewSet)
router.register(r'portfolios', viewsets.PortfolioViewSet, basename='portfolio')  # if the viewset does not include a queryset attribute we must set basename when registering the viewset.

urlpatterns = [
    path('', include(router.urls)),
    path('images/<int:image_pk>/comment', views.comment_create, name='image_comment_create'),
]
