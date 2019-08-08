from django.urls import path

from . import views

app_name = 'lendingLibrary'
urlpatterns = [
    # /lendingLibrary/
    path('', views.index, name='index'),
    # /lendingLibrary/user/1/
    path('user/<int:user_id>/', views.profile, name='profile'),
    # /lendingLibrary/user/
    path('user/', views.user, name='user'),
    # /lendingLibrary/register_login/ - login or register a user
    path('register_login/', views.register_login, name='register_login'),
    # just handles the login process, register_login renders the template
    path('register_user/', views.register_user, name='register_user'),
    # just handles the registration process, register_login renders the template
    path('login_user/', views.login_user, name='login_user'),
    # /lendingLibrary/logout_user/ - logout a user
    path('logout_user/', views.logout_user, name='logout_user'),
]
