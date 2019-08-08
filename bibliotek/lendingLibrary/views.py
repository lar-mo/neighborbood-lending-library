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

@login_required
def owner_profile(request, user_id):
    items = UserItem.objects.filter(owner_id=user_id).order_by('item_status__name', 'type__name')
    print(items)
    context = {'items': items}
    return render(request, 'lendingLibrary/owner_profile.html', context)
    # return HttpResponse('user_id' + ': ' + str(user_id))

def user(request):
    # return HttpResponse('nothing to see. move along')
    return HttpResponseRedirect(reverse('lendingLibrary:index'))
