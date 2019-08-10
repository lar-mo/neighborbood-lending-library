from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import UserItemStatus, UserItemCategory, UserItemCondition, UserItem, UserItemCheckout

def index(request):
    items = UserItem.objects.order_by('type__name').exclude(item_status__in=[6, 4])
    context = {'items': items}
    return render(request, 'lendingLibrary/index.html', context)

def profile(request, user_id):
    owner = User.objects.get(id=user_id)
    items = owner.items.order_by('item_status__name', 'type__name').exclude(item_status__in=[6, 4])
    context = {'items': items, 'owner': owner}
    return render(request, 'lendingLibrary/profile.html', context)

def category(request, category_name):
    items = UserItem.objects.filter(type__name=category_name).exclude(item_status__in=[6, 4])
    print(items)
    context = {'items': items, 'category_name': category_name}
    return render(request, 'lendingLibrary/category.html', context)

@login_required
def my_profile(request):
    owner = request.user
    item_requests = UserItemCheckout.objects.filter(checkout_status_id=1).exclude(borrower_id=owner.id)
    context = {'owner': owner, 'item_requests': item_requests}
    return render(request, 'lendingLibrary/my_profile.html', context)

@login_required
def my_checkouts(request):
    owner = request.user
    items = owner.items.order_by('item_status__name', 'type__name')
    checkouts = owner.checkouts.order_by('user_item')
    context = {'owner': owner, 'checkouts': checkouts}
    return render(request, 'lendingLibrary/my_checkouts.html', context)

@login_required
def my_items(request):
    owner = request.user
    items = owner.items.order_by('item_status__name', 'type__name')
    context = {'items': items, 'owner': owner}
    return render(request, 'lendingLibrary/my_items.html', context)

@login_required
def manage_items(request):
    owner = request.user
    items = owner.items.order_by('item_status__name', 'type__name')
    context = {'items': items, 'owner': owner}
    return render(request, 'lendingLibrary/manage_items.html', context)

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
