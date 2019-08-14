from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password

from .models import UserItemStatus, CheckoutStatus, UserItemCategory, UserItemCondition, UserItem, UserItemCheckout

def index(request):
    items = UserItem.objects.order_by('category__name').exclude(item_status__in=[6, 4])
    newest_item = UserItem.objects.filter(item_status=8).last()
    context = {'items': items, 'newest_item': newest_item}
    return render(request, 'lendingLibrary/index.html', context)

def user_items(request, user_id):
    owner = User.objects.get(id=user_id)
    items = owner.items.order_by('item_status__name', 'category__name').exclude(item_status__in=[6, 4])
    context = {'items': items, 'owner': owner}
    return render(request, 'lendingLibrary/user_items.html', context)

def category(request, category_name):
    items = UserItem.objects.filter(category__name=category_name).exclude(item_status__in=[6, 4])
    context = {'items': items, 'category_name': category_name}
    return render(request, 'lendingLibrary/category.html', context)

def item_details(request, name_slug):
    item = UserItem.objects.get(name_slug=name_slug)
    context = {'item': item}
    return render(request, 'lendingLibrary/item_details.html', context)

@login_required
def request_item(request):
    user_item_id = request.POST['user_item']
    borrower_id = request.POST['borrower']
    checkout_status = CheckoutStatus.objects.get(id=1) # 1=Pending
    item_status = UserItemStatus.objects.get(id=9) # 9=Requested
    user_item = UserItem.objects.get(id=user_item_id)
    borrower = User.objects.get(id=borrower_id)
    checkout_request_details = UserItemCheckout(user_item=user_item, borrower=borrower, checkout_status=checkout_status, request_date=timezone.now())
    checkout_request_details.save()
    user_item.item_status = item_status
    user_item.save()
    return HttpResponseRedirect(reverse('lendingLibrary:user_items', args=('3',)))

@login_required
def deny_request(request):
    checkout_status = CheckoutStatus.objects.get(id=2) # 2=Denied
    item_status = UserItemStatus.objects.get(id=8) # 8=Available
    item_request_id = request.POST['item_request_id']
    item_request = UserItemCheckout.objects.get(id=item_request_id)
    item_request.checkout_status = checkout_status
    item_request.save()
    user_item = UserItem.objects.get(id=item_request.user_item_id)
    user_item.item_status = item_status
    user_item.save()
    return HttpResponseRedirect(reverse('lendingLibrary:pending_requests'))

@login_required
def approve_request(request):
    checkout_status = CheckoutStatus.objects.get(id=3) # 3=Active
    item_status = UserItemStatus.objects.get(id=10) # 10=Checked Out
    due_date = request.POST['due_date']
    item_request_id = request.POST['item_request_id']
    item_request = UserItemCheckout.objects.get(id=item_request_id)
    item_request.checkout_status = checkout_status
    item_request.checkout_date = timezone.now()
    item_request.due_date = due_date
    item_request.save()
    user_item = UserItem.objects.get(id=item_request.user_item_id)
    user_item.item_status = item_status
    user_item.save()
    return HttpResponseRedirect(reverse('lendingLibrary:pending_requests'))

@login_required
def my_profile(request):
    user_info = request.user
    message = request.GET.get('message', '').strip()
    context = {'user_info': user_info, 'message': message}
    return render(request, 'lendingLibrary/my_profile.html', context)

def save_info(request):
    user_info = User.objects.get(id=request.user.id)
    user_info.first_name = request.POST['first_name'].strip()
    user_info.last_name = request.POST['last_name'].strip()
    user_info.email = request.POST['email'].strip()
    user_info.save()
    return HttpResponseRedirect(reverse('lendingLibrary:my_profile')+'?message=info_saved')

def save_password(request):
    # authenticate that old password is correct
    old_password = request.POST['old_password'].strip()
    current_password = request.user.password
    success = check_password(old_password, current_password)
    if not success:
        return HttpResponseRedirect(reverse('lendingLibrary:my_profile')+'?message=bad_password')
    else:
        # if True,
        new_password = request.POST['new_password'].strip()
        user = User.objects.get(id=request.user.id)
        user.set_password(new_password)
        user.save()
        login(request, user)
        return HttpResponseRedirect(reverse('lendingLibrary:my_profile')+'?message=password_saved')

def check_pwd(request):
    current_password = request.user.password
    typed_password = request.POST['typed_password'].strip()
    success = check_password(typed_password, current_password)
    if success:
        return HttpResponseRedirect(reverse('lendingLibrary:my_profile')+'?message=good_password')
    else:
        return HttpResponseRedirect(reverse('lendingLibrary:my_profile')+'?message=bad_password2')

@login_required
def pending_requests(request):
    owner = request.user
    pending_requests = UserItemCheckout.objects.filter(checkout_status_id=1).exclude(borrower_id=owner.id)
    context = {'owner': owner, 'pending_requests': pending_requests}
    return render(request, 'lendingLibrary/pending_requests.html', context)

@login_required
def my_checkouts(request):
    owner = request.user
    items = owner.items.order_by('item_status__name', 'category__name')
    checkouts = owner.checkouts.order_by('user_item')
    context = {'owner': owner, 'checkouts': checkouts}
    return render(request, 'lendingLibrary/my_checkouts.html', context)

@login_required
def my_items(request):
    owner = request.user
    items = owner.items.order_by('item_status__name', 'category__name')
    item_requests = UserItemCheckout.objects.filter(user_item__in=items).exclude(checkout_status=2)
    filter = ['Available', 'Unavailable', 'Lost', 'Hidden']
    context = {'items': items, 'owner': owner, 'item_requests': item_requests, 'filter': filter}
    return render(request, 'lendingLibrary/my_items.html', context)

@login_required
def manage_items(request):
    owner = request.user
    items = owner.items.order_by('item_status__name', 'category__name')
    context = {'items': items, 'owner': owner}
    return render(request, 'lendingLibrary/manage_items.html', context)

@login_required
def new_item(request):
    owner = request.user
    items = owner.items.order_by('item_status__name', 'category__name')
    categories = UserItemCategory.objects.order_by('name')
    conditions = UserItemCondition.objects.order_by('id')
    context = {'categories': categories, 'conditions': conditions, 'items': items, 'owner': owner}
    return render(request, 'lendingLibrary/new_item.html', context)

def create_new_item(request):
    name = request.POST['name'].strip()
    description = request.POST['description'].strip()
    image_url = request.POST['image_url'].strip()
    category_id = request.POST['category']
    condition_id = request.POST['condition']
    replacement_cost = request.POST['replacement_cost']
    item_status_id = request.POST['item_status']
    name_slug = request.POST['name_slug']
    owner = request.user
    new_user_item = UserItem(name=name, description=description, image_url=image_url, category_id=category_id, condition_id=condition_id, replacement_cost=replacement_cost, item_status_id=item_status_id, name_slug=name_slug, owner=owner)
    new_user_item.save()
    return HttpResponseRedirect(reverse('lendingLibrary:my_items'))

@login_required
def edit_item(request, item_id):
    owner = request.user
    item = owner.items.get(id=item_id)
    items = owner.items.order_by('item_status__name', 'category__name')
    categories = UserItemCategory.objects.order_by('name')
    conditions = UserItemCondition.objects.order_by('id')
    item_statuses = UserItemStatus.objects.order_by('name').exclude(id__in=[9, 10])
    context = {'item': item, 'items': items, 'categories': categories, 'conditions': conditions, 'item_statuses': item_statuses}
    return render(request, 'lendingLibrary/edit_item.html', context)

@login_required
def save_edited_item(request):
    # return HttpResponse('ok')
    user_item_id = request.POST['item_id']
    owner = request.user
    user_item = owner.items.get(id=user_item_id)
    user_item.name = request.POST['name'].strip()
    user_item.description = request.POST['description'].strip()
    user_item.image_url = request.POST['image_url'].strip()
    user_item.category_id = request.POST['category']
    user_item.condition_id = request.POST['condition']
    user_item.replacement_cost = request.POST['replacement_cost']
    user_item.item_status_id = request.POST['item_status']
    user_item.save()
    return HttpResponseRedirect(reverse('lendingLibrary:my_items'))

def delete_item(request):
    user_item_id = request.POST['user_items']
    user_item = UserItem.objects.get(id=user_item_id)
    user_item.delete()
    return HttpResponseRedirect(reverse('lendingLibrary:manage_items'))

def user(request):
    # nothing to see. move along
    return HttpResponseRedirect(reverse('lendingLibrary:index'))

def edititem(request):
    # nothing to see. move along
    return HttpResponseRedirect(reverse('lendingLibrary:manage_items'))

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
