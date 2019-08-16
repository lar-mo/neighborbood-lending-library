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

    # /lendingLibrary/category/Books/
    path('category/<str:category_name>/', views.category, name='category'),

    # /lendingLibrary/item/18/ratchet-and-socket-set/
    path('item/<int:item_id>/<str:name_slug>/', views.item_details, name='item_details'),

    # /lendingLibrary/item/ - error handling, show item detail page anyway
    path('item/<int:item_id>/', views.item_details_no_slug, name='item_details_no_slug'),

    # /lendingLibrary/item/ - error handling, redirect to index if trying to go to / (index)
    path('item/', views.item, name='item'),

    # /lendingLibrary/search/ - search results
    path('search/', views.search_results, name='search_results'),

    # /lendingLibrary/search/ - search results
    # path('search/', views.search_results_q, name='search_results_q'),

    # /lendingLibrary/search/tent/ - search results
    path('search/<str:search_term>/', views.search_results_keyword, name='search_results_keyword'),

    # /lendingLibrary/request_item/ - form handling
    path('request_item/', views.request_item, name='request_item'),

    # /lendingLibrary/deny_request/ - form handling
    path('deny_request/', views.deny_request, name='deny_request'),

    # /lendingLibrary/approve_request/ - form handling
    path('approve_request/', views.approve_request, name='approve_request'),

    # /lendingLibrary/item_check_in/ - form handling
    path('item_check_in/', views.item_check_in, name='item_check_in'),

    # /lendingLibrary/my_profile/ - logged in user's profile - view & edit profile (name, email, password)
    path('my_profile/', views.my_profile, name='my_profile'),

    # /lendingLibrary/save_info/ - form handling
    path('save_info/', views.save_info, name='save_info'),

    # /lendingLibrary/save_password/ - form handling
    path('save_password/', views.save_password, name='save_password'),

    # /lendingLibrary/check_password/ - TEST - check password
    path('check_password/', views.check_pwd, name='check_pwd'),

    # /lendingLibrary/pending_requests/ - logged in user's profile - borrower requests
    path('pending_requests/', views.pending_requests, name='pending_requests'),

    # /lendingLibrary/my_checkouts/ - logged in user's profile - my requests & checkouts
    path('my_checkouts/', views.my_checkouts, name='my_checkouts'),

    # /lendingLibrary/my_items/ - logged in user's profile - see my items
    path('my_items/', views.my_items, name='my_items'),

    # /lendingLibrary/manage_items/ - logged in user's profile - manage items
    path('manage_items/', views.manage_items, name='manage_items'),

    # /lendingLibrary/new_item/ - logged in user's profile - add item form
    path('new_item/', views.new_item, name='new_item'),

    # /lendingLibrary/create_new_item/ - form handling
    path('create_new_item/', views.create_new_item, name='create_new_item'),

    # /lendingLibrary/edit_item/10/ - edit item form
    path('edit_item/<int:item_id>/', views.edit_item, name='edit_item'),

    # /lendingLibrary/edit_item/ - error handling, redirect to manage_items if trying to go to /edit_item/
    path('edit_item/', views.edititem, name='edititem'),

    # /lendingLibrary/save_edited_item/ - form handling
    path('save_edited_item/', views.save_edited_item, name='save_edited_item'),

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
