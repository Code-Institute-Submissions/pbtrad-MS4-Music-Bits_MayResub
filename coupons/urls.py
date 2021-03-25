from django.conf.urls import url
from .import views
from django.urls import path


urlpatterns = [
path('', views.coupon_apply, name='coupon_apply'),
]