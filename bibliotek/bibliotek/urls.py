from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('lendingLibrary/', include('lendingLibrary.urls')),
    path('admin/', admin.site.urls),
]
