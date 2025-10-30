from django.urls import path
from . import views

urlpatterns = [
    path('districts/', views.district_list, name='district_list'),
    path('performance/<str:district_name>/', views.district_performance, name='district_performance'),
    path('initialize/', views.initialize_data, name='initialize_data'),
    path('detect-district/', views.detect_district, name='detect_district'),
]