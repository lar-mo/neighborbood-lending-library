from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password

from .models import UserItemStatus, CheckoutStatus, UserItemCategory, UserItemCondition, UserItem, UserItemCheckout

def index(request):
    items = UserItem.objects.order_by('category__name').exclude(item_status__name__in=['Hidden', 'Lost'])
    if not request.user.username == "":
        newest_items = UserItem.objects.filter(item_status__name='Available').exclude(owner=request.user).order_by('-id')[:3:1]
    else:
        newest_items = UserItem.objects.filter(item_status__name='Available').order_by('-id')[:3:1]
    categories = UserItemCategory.objects.order_by('name')
    context = {'items': items, 'newest_items': newest_items, 'categories': categories}
    return render(request, 'lendingLibrary/index.html', context)

def user_items(request, user_id):
    owner = User.objects.get(id=user_id)
    items = owner.items.order_by('item_status__name', 'category__name').exclude(item_status__name__in=['Hidden', 'Lost'])
    categories = UserItemCategory.objects.order_by('name')
    context = {'items': items, 'owner': owner, 'categories': categories}
    return render(request, 'lendingLibrary/user_items.html', context)

def category(request, category_name):
    items = UserItem.objects.filter(category__name=category_name).exclude(item_status__name__in=['Hidden', 'Lost'])
    categories = UserItemCategory.objects.order_by('name')
    context = {'items': items, 'category_name': category_name, 'categories': categories}
    return render(request, 'lendingLibrary/category.html', context)

def item_details(request, item_id, name_slug):
    item = UserItem.objects.get(id=item_id)
    categories = UserItemCategory.objects.order_by('name')
    context = {'item': item, 'categories': categories}
    return render(request, 'lendingLibrary/item_details.html', context)

def item_details_no_slug(request, item_id):
    item = UserItem.objects.get(id=item_id)
    context = {'item': item}
    return render(request, 'lendingLibrary/item_details.html', context)

# def search_results(request):
#     search_term = request.POST['q']
#     items = UserItem.objects.filter(name__contains=search_term).exclude(item_status__name__in=['Hidden', 'Lost']) | UserItem.objects.filter(description__contains=search_term).exclude(item_status__name__in=['Hidden', 'Lost'])
#     context = {'items': items, 'search_term': search_term}
#     return render(request, 'lendingLibrary/search_results.html', context)

def search_results(request):
    search_term = request.GET['q']
    items_filtered = UserItem.objects.exclude(item_status__name__in=['Hidden', 'Lost'])
    items = items_filtered.filter(name__iregex=r'\b{0}\b'.format(search_term)) | items_filtered.filter(description__iregex=r'\b{0}\b'.format(search_term)) ## whole word match, e.g. 'mat' => 'on', not 'one', 'won' ##
    # items = items_filtered.filter(name__contains=search_term) | items_filtered.filter(description__contains=search_term) ## partial match, e.g. 'on' => 'won', 'one', 'on' ##
    categories = UserItemCategory.objects.order_by('name')
    context = {'items': items, 'search_term': search_term, 'categories': categories}
    return render(request, 'lendingLibrary/search_results.html', context)

def search_results_keyword(request, search_term):
    items = UserItem.objects.filter(name__contains=search_term).exclude(item_status__name__in=['Hidden', 'Lost']) | UserItem.objects.filter(description__contains=search_term).exclude(item_status__name__in=['Hidden', 'Lost'])
    categories = UserItemCategory.objects.order_by('name')
    context = {'items': items, 'search_term': search_term, 'categories': categories}
    return render(request, 'lendingLibrary/search_results.html', context)

@login_required
def request_item(request):
    open_request_count = UserItemCheckout.objects.filter(borrower=request.user.id, checkout_status__name__in=['Pending', 'Active']).count()
    if open_request_count >= 4: #limits user to 4 Pending or Active items
        return HttpResponseRedirect(reverse('lendingLibrary:my_checkouts')+'?message=over_request_limit')
    else:
        user_item_id = request.POST['user_item']
        borrower_id = request.POST['borrower']
        checkout_status = CheckoutStatus.objects.get(name='Pending')
        item_status = UserItemStatus.objects.get(name='Requested')
        user_item = UserItem.objects.get(id=user_item_id)
        borrower = User.objects.get(id=borrower_id)
        checkout_request_details = UserItemCheckout(user_item=user_item, borrower=borrower, checkout_status=checkout_status, request_date=timezone.now())
        checkout_request_details.save()
        user_item.item_status = item_status
        user_item.save()

        subject = 'Item Requested'
        msg_plain = 'Your item [' + user_item.name + '] was requested by ' + borrower.username.capitalize() + '.'
        sender = 'Postmaster <postmaster@community-lending-library.org>'
        recipient = [user_item.owner.email]
        msg_html = '<h1>Your item <u><i>' + user_item.name + '</i></u> was was requested by ' + borrower.username.capitalize() + '.</h1>'
        try:
            send_mail(subject, msg_plain, sender, recipient, fail_silently=False, html_message=msg_html)
        except:
            print('!!! There was an error sending an email! !!!')

        subject = 'Item Requested'
        msg_plain = 'Your request for [' + user_item.name + '] was sent to ' + user_item.owner.username.capitalize() + '.'
        sender = 'Postmaster <postmaster@community-lending-library.org>'
        recipient = [borrower.email]
        msg_html = '<h1>Your request for <u><i>' + user_item.name + '</i></u> was sent to ' + user_item.owner.username.capitalize() + '.</h1>'
        try:
            send_mail(subject, msg_plain, sender, recipient, fail_silently=False, html_message=msg_html)
        except:
            print('!!! There was an error sending an email! !!!')

        return HttpResponseRedirect(reverse('lendingLibrary:my_checkouts'))

@login_required
def deny_request(request):
    checkout_status = CheckoutStatus.objects.get(name='Denied')
    item_status = UserItemStatus.objects.get(name='Available')
    deny_reason = request.POST['deny_reason']
    item_request_id = request.POST['item_request_id']
    item_request = UserItemCheckout.objects.get(id=item_request_id)
    item_request.checkout_status = checkout_status
    item_request.reason = deny_reason
    item_request.save()
    user_item = UserItem.objects.get(id=item_request.user_item_id)
    user_item.item_status = item_status
    user_item.save()

    subject = 'Item Request Declined'
    msg_plain = 'Your request for [' + user_item.name + '] was declined.\nReason: ' + deny_reason
    sender = 'Postmaster <postmaster@community-lending-library.org>'
    recipient = [item_request.borrower.email]
    msg_html = '<h1>Your request for <u><i>' + user_item.name + '</i></u> was declined.</h1><h3>Reason: ' + deny_reason + '</h3>'
    try:
        send_mail(subject, msg_plain, sender, recipient, fail_silently=False, html_message=msg_html)
    except:
        print('!!! There was an error sending an email! !!!')

    return HttpResponseRedirect(reverse('lendingLibrary:pending_requests'))

@login_required
def approve_request(request):
    checkout_status = CheckoutStatus.objects.get(name='Active')
    item_status = UserItemStatus.objects.get(name='Checked Out')
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

    subject = 'Item Request Approved'
    msg_plain = 'Your request for [' + user_item.name + '] was approved.\nThe due date is ' + item_request.due_date + '.'
    sender = 'Postmaster <postmaster@community-lending-library.org>'
    recipient = [item_request.borrower.email]
    msg_html = '<h1>Your request for <u><i>' + user_item.name + '</i></u> was approved.</h1><h3>The due date is ' + item_request.due_date + '.</h3>'
    try:
        send_mail(subject, msg_plain, sender, recipient, fail_silently=False, html_message=msg_html)
    except:
        print('!!! There was an error sending an email! !!!')

    return HttpResponseRedirect(reverse('lendingLibrary:pending_requests'))

@login_required
def item_check_in(request):
    checkout_status = CheckoutStatus.objects.get(name='Completed')
    item_status = UserItemStatus.objects.get(name='Available')
    item_request_id = request.POST['item_request_id']
    item_request = UserItemCheckout.objects.get(id=item_request_id)
    item_request.checkout_status = checkout_status
    item_request.checkin_date = timezone.now()
    item_request.save()
    user_item = UserItem.objects.get(id=item_request.user_item_id)
    user_item.item_status = item_status
    user_item.save()

    subject = 'Item Returned'
    msg_plain = '[' + user_item.name + '] was received by ' + user_item.owner.username.capitalize() + '.'
    sender = 'Postmaster <postmaster@community-lending-library.org>'
    recipient = [item_request.borrower.email]
    msg_html = '<h1><u><i>' + user_item.name + '</i></u> was received by ' + user_item.owner.username.capitalize() + '.</h1>'
    try:
        send_mail(subject, msg_plain, sender, recipient, fail_silently=False, html_message=msg_html)
    except:
        print('!!! There was an error sending an email! !!!')

    return HttpResponseRedirect(reverse('lendingLibrary:my_items'))

@login_required
def my_profile(request):
    user_info = request.user
    message = request.GET.get('message', '').strip()
    categories = UserItemCategory.objects.order_by('name')
    context = {'user_info': user_info, 'message': message, 'categories': categories}
    return render(request, 'lendingLibrary/my_profile.html', context)

def save_info(request):
    user_info = User.objects.get(id=request.user.id)
    user_info.first_name = request.POST['first_name'].strip()
    user_info.last_name = request.POST['last_name'].strip()
    user_info.email = request.POST['email'].strip()
    user_info.save()

    subject = 'Profile Info Updated'
    msg_plain = 'Your profile information was updated.'
    sender = 'Postmaster <postmaster@community-lending-library.org>'
    recipient = [user_info.email]
    msg_html = '<h1>Your profile information was updated.</h1>'
    try:
        send_mail(subject, msg_plain, sender, recipient, fail_silently=False, html_message=msg_html)
    except:
        print('!!! There was an error sending an email! !!!')

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

        subject = 'Password Changed'
        msg_plain = 'Your password was changed.'
        sender = 'Postmaster <postmaster@community-lending-library.org>'
        recipient = [user.email]
        msg_html = '<h1>Your password was changed.</h1>'
        try:
            send_mail(subject, msg_plain, sender, recipient, fail_silently=False, html_message=msg_html)
        except:
            print('!!! There was an error sending an email! !!!')

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
    pending_requests = UserItemCheckout.objects.filter(checkout_status__name='Pending', user_item__owner=owner.id).exclude(borrower_id=owner.id).order_by('-request_date')
    tomorrows_date = timezone.now() + timezone.timedelta(days=1)
    categories = UserItemCategory.objects.order_by('name')
    context = {'owner': owner, 'pending_requests': pending_requests, 'tomorrows_date': tomorrows_date, 'categories': categories}
    return render(request, 'lendingLibrary/pending_requests.html', context)

@login_required
def my_checkouts(request):
    message = request.GET.get('message', '')
    owner = request.user
    items = owner.items.order_by('item_status__name', 'category__name')
    checkouts = owner.checkouts.order_by('-request_date')#.exclude(user_item__owner=request.user)
    categories = UserItemCategory.objects.order_by('name')
    context = {'owner': owner, 'checkouts': checkouts, 'message': message, 'categories': categories}
    return render(request, 'lendingLibrary/my_checkouts.html', context)

@login_required
def my_items(request):
    owner = request.user
    items = owner.items.order_by('-item_status__name', 'category__name')
    item_requests = UserItemCheckout.objects.filter(user_item__in=items).order_by('checkout_status__name', '-due_date')
    categories = UserItemCategory.objects.order_by('name')
    context = {'owner': owner, 'items': items, 'item_requests': item_requests, 'categories': categories}
    return render(request, 'lendingLibrary/my_items.html', context)

@login_required
def manage_items(request):
    owner = request.user
    items = owner.items.order_by('item_status__name', 'category__name')
    categories = UserItemCategory.objects.order_by('name')
    context = {'items': items, 'owner': owner, 'categories': categories}
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
    image = request.FILES['image']
    category_id = request.POST['category']
    condition_id = request.POST['condition']
    replacement_cost = request.POST['replacement_cost']
    item_status_id = request.POST['item_status']
    owner = request.user
    new_user_item = UserItem(name=name, description=description, image=image, category_id=category_id, condition_id=condition_id, replacement_cost=replacement_cost, item_status_id=item_status_id, owner=owner)
    new_user_item.save()

    subject = 'New Item Added'
    msg_plain = 'Your item [' + name + '] was added to the catalog.'
    sender = 'Postmaster <postmaster@community-lending-library.org>'
    recipient = [owner.email]
    msg_html = '<h1>Your item <u><i>' + name + '</i></u> was added to the catalog.</h1>'
    try:
        send_mail(subject, msg_plain, sender, recipient, fail_silently=False, html_message=msg_html)
    except:
        print('!!! There was an error sending an email! !!!')

    return HttpResponseRedirect(reverse('lendingLibrary:my_items'))

@login_required
def edit_item(request, item_id):
    owner = request.user
    item = owner.items.get(id=item_id)
    items = owner.items.order_by('item_status__name', 'category__name')
    categories = UserItemCategory.objects.order_by('name')
    conditions = UserItemCondition.objects.order_by('id')
    item_statuses = UserItemStatus.objects.order_by('name').exclude(name__in=['Requested', 'Checked Out'])
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
    user_item.image = request.FILES['image']
    user_item.category_id = request.POST['category']
    user_item.condition_id = request.POST['condition']
    user_item.replacement_cost = request.POST['replacement_cost']
    user_item.item_status_id = request.POST['item_status']
    user_item.save()

    subject = 'Item Details Updated'
    msg_plain = 'Your item [' + user_item.name + '] was updated.'
    sender = 'Postmaster <postmaster@community-lending-library.org>'
    recipient = [user_item.owner.email]
    msg_html = '<h1>Your item <u><i>' + user_item.name + '</i></u> was updated.</h1>'
    try:
        send_mail(subject, msg_plain, sender, recipient, fail_silently=False, html_message=msg_html)
    except:
        print('!!! There was an error sending an email! !!!')

    return HttpResponseRedirect(reverse('lendingLibrary:my_items'))

def delete_item(request):
    user_item_id = request.POST['user_items']
    user_item = UserItem.objects.get(id=user_item_id)
    user_item.delete()

    subject = 'Item Deleted'
    msg_plain = render_to_string('lendingLibrary/email.txt', {'page': 'itm_del', 'user_item': user_item})
    sender = 'Postmaster <postmaster@community-lending-library.org>'
    recipient = [user_item.owner.email]
    msg_html = render_to_string('lendingLibrary/email.html', {'page': 'itm_del', 'user_item': user_item})
    try:
        send_mail(subject, msg_plain, sender, recipient, fail_silently=False, html_message=msg_html)
    except:
        print('!!! There was an error sending an email! !!!')

    return HttpResponseRedirect(reverse('lendingLibrary:manage_items'))

def user(request):
    # nothing to see. move along
    return HttpResponseRedirect(reverse('lendingLibrary:index'))

def edititem(request):
    # nothing to see. move along
    return HttpResponseRedirect(reverse('lendingLibrary:manage_items'))

def item(request):
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

    subject = 'New Registration'
    msg_plain = render_to_string('lendingLibrary/email.txt', {'page': 'new_reg', 'username': username})
    sender = 'Postmaster <postmaster@community-lending-library.org>'
    recipient = [email]
    msg_html = render_to_string('lendingLibrary/email.html', {'page': 'new_reg', 'username': username})
    try:
        send_mail(subject, msg_plain, sender, recipient, fail_silently=False, html_message=msg_html)
    except:
        print('!!! There was an error sending an email! !!!')

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

def about(request):
    categories = UserItemCategory.objects.order_by('name')
    context = {'categories': categories}
    return render(request, 'lendingLibrary/about.html', context)

def tos(request):
    categories = UserItemCategory.objects.order_by('name')
    context = {'categories': categories}
    return render(request, 'lendingLibrary/terms_of_service.html', context)

def image_upload(request):
    # return HttpResponse('ok')
    # items = UserItem.objects.order_by('category__name')
    item = UserItem.objects.get(id='35')
    category = item.category.name

    subject = 'Test'
    msg_plain = render_to_string('lendingLibrary/email.txt', {'category': item.category.name, 'item': item.name, 'owner': item.owner.username, 'page': 'test'})
    sender = 'Postmaster <postmaster@community-lending-library.org>'
    recipient = [item.owner.email]
    msg_html = render_to_string('lendingLibrary/email.html', {'category': item.category.name, 'item': item.name, 'page': 'test'})

    try:
        send_mail(subject, msg_plain, sender, recipient, fail_silently=False, html_message=msg_html)
    except:
        print('!!! There was an error sending an email! !!!')

    context = {'item': item, 'category': category}
    return render(request, 'lendingLibrary/image_upload.html', context)
