# urls.py

from django.urls import path
from . import views



urlpatterns = [
    path('', views.show_map, name='show_map'),
    path('save_location/', views.save_location, name='save_location'),
    path('resolve_incident/<int:location_id>/', views.resolve_incident, name='resolve_incident'),
    # path('map_statistic/', views.map_statistic, name='map_statistic'),

]
