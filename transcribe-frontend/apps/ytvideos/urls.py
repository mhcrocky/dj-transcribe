# backend/server/apps/ytvideos/urls.py
from django.urls import path, re_path
from django.conf.urls import url, include 
from rest_framework.routers import DefaultRouter
from apps.ytvideos.views import YtvideoViewSet
from . import views

router = DefaultRouter()
router.register("ytvideos", YtvideoViewSet, basename="ytvideos")
ytvideos_urlpatterns = [url("api/v1/", include(router.urls))]

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('success/', views.SuccessView.as_view()),
    path('cancelled/', views.CancelledView.as_view()),
    path('config/', views.stripe_config),
    path('ytvideo-info/', views.retrieve_ytvideo_info),
    path('create-checkout-session/', views.create_checkout_session),
    path('create-checkout-mp3-session/', views.create_checkout_mp3_session),
    path('webhook/', views.stripe_webhook),
    re_path(r'^(?:.*)/?$', views.HomePageView.as_view()),
]
