from django.urls import path

from . import views

app_name = 'lendingLibrary'
urlpatterns = [
    # /lendingLibrary/
    path('', views.index, name='index'),

    # /lendingLibrary/user/1/
    path('user/<int:user_id>/', views.user_items, name='user_items'),

    # /lendingLibrary/user/ - error handling, redirect to index if trying to go to /user/
    path('user/', views.user, name='user'),

    # /lendingLibrary/category/books/
    path('category/<str:category_name>/', views.category, name='category'),

    # /lendingLibrary/request_item/ - form handling
    path('request_item/', views.request_item, name='request_item'),

    # /lendingLibrary/deny_request/ - form handling
    path('deny_request/', views.deny_request, name='deny_request'),

    # /lendingLibrary/approve_request/ - form handling
    path('approve_request/', views.approve_request, name='approve_request'),

    # /lendingLibrary/my_profile/ - logged in user's profile - view & edit profile (name, email, password)
    path('my_profile/', views.my_profile, name='my_profile'),

    # /lendingLibrary/save_info/ - form handling
    path('save_info/', views.save_info, name='save_info'),

    # /lendingLibrary/save_password/ - form handling
    path('save_password/', views.save_password, name='save_password'),

    # /lendingLibrary/check_password/ - TEST - check password
    path('check_password/', views.check_pwd, name='check_pwd'),

    # /lendingLibrary/pending_requests/ - logged in user's profile - borrower requests
    path('pending_requests/', views.item_requests, name='item_requests'),

    # /lendingLibrary/my_checkouts/ - logged in user's profile - my requests & checkouts
    path('my_checkouts/', views.my_checkouts, name='my_checkouts'),

    # /lendingLibrary/my_items/ - logged in user's profile - see my items
    path('my_items/', views.my_items, name='my_items'),

    # /lendingLibrary/manage_items/ - logged in user's profile - manage items
    path('manage_items/', views.manage_items, name='manage_items'),

    # /lendingLibrary/delete_item/ - form handling
    path('delete_item/', views.delete_item, name='delete_item'),

    # /lendingLibrary/register_login/ - login or register a user
    path('register_login/', views.register_login, name='register_login'),

    # just handles the login process, register_login renders the template
    path('register_user/', views.register_user, name='register_user'),

    # just handles the registration process, register_login renders the template
    path('login_user/', views.login_user, name='login_user'),

    # /lendingLibrary/logout_user/ - logout a user
    path('logout_user/', views.logout_user, name='logout_user'),
]
