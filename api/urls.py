from django.urls import path, include

urlpatterns = [
    path("users/",include("users.urls")),
    path('tests/',include('main.urls')),
    path('raiting/', include('users.raiting_urls')),]