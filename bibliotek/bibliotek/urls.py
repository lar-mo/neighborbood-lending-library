from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    #remove lendingLibrary if hosted on it's own domain
    path('', include('lendingLibrary.urls')),
    path('admin/', admin.site.urls),
]
