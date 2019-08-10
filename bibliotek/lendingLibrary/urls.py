from django.urls import path

from . import views

app_name = 'lendingLibrary'
urlpatterns = [
    # /lendingLibrary/
    path('', views.index, name='index'),

    # /lendingLibrary/user/1/
    path('user/<int:user_id>/', views.profile, name='profile'),

    # # /lendingLibrary/category/books/
    path('category/<str:category_name>/', views.category, name='category'),

    # /lendingLibrary/user/ - error handling, redirect to index if trying to go to /user/
    path('user/', views.user, name='user'),

    # /lendingLibrary/my_profile/ - logged in user's profile - borrower requests
    path('my_profile/', views.my_profile, name='my_profile'),

    # /lendingLibrary/my_checkouts/ - logged in user's profile - my requests & checkouts
    path('my_checkouts/', views.my_checkouts, name='my_checkouts'),

    # /lendingLibrary/my_items/ - logged in user's profile - see my items
    path('my_items/', views.my_items, name='my_items'),

    # /lendingLibrary/my_items/ - logged in user's profile - manage items
    path('manage_items/', views.manage_items, name='manage_items'),

    # /lendingLibrary/register_login/ - login or register a user
    path('register_login/', views.register_login, name='register_login'),

    # just handles the login process, register_login renders the template
    path('register_user/', views.register_user, name='register_user'),

    # just handles the registration process, register_login renders the template
    path('login_user/', views.login_user, name='login_user'),

    # /lendingLibrary/logout_user/ - logout a user
    path('logout_user/', views.logout_user, name='logout_user'),
]
