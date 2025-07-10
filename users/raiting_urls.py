from django.urls import path
from .views import (
    StudentAllRaitingView,
    StudentCityRaitingView,
    StudentRegionRaitingView,
    StudentSchoolRaitingView,
)

urlpatterns = [
    path('students/raiting', StudentAllRaitingView.as_view(), name='raiting'),
    path('students/city/raiting', StudentCityRaitingView.as_view(), name='city-raiting'),
    path('students/region/raiting', StudentRegionRaitingView.as_view(), name='region-raiting'),
    path('students/school/raiting', StudentSchoolRaitingView.as_view(), name='school-raiting'),

]