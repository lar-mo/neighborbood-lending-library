from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import UserItemStatus, UserItemCategory, UserItemCondition, UserItem, UserItemCheckout

def index(request):
    items = UserItem.objects.order_by('type__name').exclude(item_status__in=[6, 4])
    message = request.GET.get('message', '')
    next = request.GET.get('next', '')
    context = {'items': items, 'message': message,'next': next}
    return render(request, 'lendingLibrary/index.html', context)

def profile(request, user_id):
    owner = User.objects.get(id=user_id)
    items = owner.items.order_by('item_status__name', 'type__name').exclude(item_status__in=[6, 4])
    context = {'items': items, 'owner': owner}
    return render(request, 'lendingLibrary/profile.html', context)

@login_required
def my_profile(request):
    owner = request.user
    items = owner.items.order_by('item_status__name', 'type__name')
    item_requests = UserItemCheckout.objects.order_by('user_item').exclude(checkout_status_id__in=[2, 3])
    print("!!!")
    print(item_requests)
    # checkouts = UserItemCheckout.objects.filter(borrower=owner).order_by('user_item') # method 1
    # checkouts = owner.useritemcheckout_set.order_by('user_item')                      # method 2
    checkouts = owner.checkouts.order_by('user_item')                                   # method 3
    context = {'items': items, 'owner': owner, 'item_requests': item_requests, 'checkouts': checkouts}
    return render(request, 'lendingLibrary/my_profile.html', context)

def user(request):
    # nothing to see. move along
    return HttpResponseRedirect(reverse('lendingLibrary:index'))

def register_login(request):
    message = request.GET.get('message', '')
    next = request.GET.get('next', '')
    context = {
        'message': message,
        'next': next
    }
    return render(request, 'lendingLibrary/register_login.html', context)

def register_user(request):
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    next = request.POST['next']

    user = User.objects.create_user(username, email, password)
    login(request, user)

    if next != '':
        return HttpResponseRedirect(next)
    return HttpResponseRedirect(reverse('lendingLibrary:index'))

def login_user(request):
    username = request.POST['username']
    password = request.POST['password']
    next = request.POST['next']
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        if next != '':
            return HttpResponseRedirect(next)
        return HttpResponseRedirect(reverse('lendingLibrary:owner_profile'))

    if next != '':
        return HttpResponseRedirect(reverse('lendingLibrary:register_login')+'?message=fail&next='+next)
    return HttpResponseRedirect(reverse('lendingLibrary:register_login')+'?message=fail')

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('lendingLibrary:index')+'?message=logout')
