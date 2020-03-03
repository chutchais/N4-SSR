from django.contrib import admin
from django.urls import path


from .views import SsrFilesDetailView

urlpatterns = [
    path('ssrfile/<int:pk>', SsrFilesDetailView.as_view(), name='ssrfiles-detail'),
]
