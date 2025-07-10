from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView 
from .views import  (
    CustomTokenObtainPairView,
    RegisterView,
    LogoutView,
    ShowTeacherStudents,
    EditStudentsView,
)


urlpatterns = [
    path('teacher/students/<int:id>/edit/', EditStudentsView.as_view(), name='edit-students'),
    path('teacher/students/', ShowTeacherStudents.as_view(), name='show-students'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(),name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
]