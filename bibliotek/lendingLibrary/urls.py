from django.urls import path

from . import views

app_name = 'lendingLibrary'
urlpatterns = [
    # /lendingLibrary/
    path('', views.index, name='index'),

    # /lendingLibrary/user/1/
    path('user/<int:user_id>/', views.profile, name='profile'),

    # # /lendingLibrary/user/1/
    # path('owner/<int:user_id>/', views.owner_profile, name='owner_profile'),

    # /lendingLibrary/user/ - error handling, redirect to index if trying to go to /user/
    path('user/', views.user, name='user'),

    # /lendingLibrary/user/ - error handling, redirect to index if trying to go to /user/
    path('owner/', views.owner_profile, name='owner_profile'),

    # /lendingLibrary/register_login/ - login or register a user
    path('register_login/', views.register_login, name='register_login'),

    # just handles the login process, register_login renders the template
    path('register_user/', views.register_user, name='register_user'),

    # just handles the registration process, register_login renders the template
    path('login_user/', views.login_user, name='login_user'),

    # /lendingLibrary/logout_user/ - logout a user
    path('logout_user/', views.logout_user, name='logout_user'),
]
