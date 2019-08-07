from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone

from .models import UserItemStatus, UserItemCategory, UserItemCondition, UserItem, UserItemCheckout

def index(request):
    items = UserItem.objects.order_by('type').exclude(item_status=6)
    context = {'items': items}
    return render(request, 'lendingLibrary/index.html', context)
