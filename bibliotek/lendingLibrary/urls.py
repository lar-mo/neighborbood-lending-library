from django.urls import path

from . import views

app_name = 'lendingLibrary'
urlpatterns = [
    # /lendingLibrary/
    path('', views.index, name='index'),
    # /lendingLibrary/user/1/
    path('user/<int:user_id>/', views.owner_profile, name='owner_profile'),
    # /lendingLibrary/user/
    path('user/', views.user, name='user'),
]
