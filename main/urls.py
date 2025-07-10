from django.urls import path
from .views import (
    TestCasesView,
    TestsView
)

urlpatterns = [
    path('', TestCasesView.as_view(), name='test-cases'),
    path('check/<int:id>/', TestsView.as_view(), name='test'),
]