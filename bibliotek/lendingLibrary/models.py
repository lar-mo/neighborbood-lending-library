from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


def pending_requests_count(user):
    number_of_pending_requests = user.items.filter(item_status=9).count()
    return number_of_pending_requests
User.add_to_class('pending_requests_count', pending_requests_count)

def my_checkouts_count(user):
    number_of_my_checkouts= user.checkouts.exclude(checkout_status__in=[2,4]).count()
    return number_of_my_checkouts
User.add_to_class('my_checkouts_count', my_checkouts_count)

def my_items_available_count(user):
    number_of_available_items = user.items.filter(item_status=8).count()
    return number_of_available_items
User.add_to_class('my_items_available_count', my_items_available_count)

def my_items_total_count(user):
    return user.items.count()
User.add_to_class('my_items_total_count', my_items_total_count)

class UserItemStatus(models.Model):
    name            = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class CheckoutStatus(models.Model):
    name            = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class UserItemCategory(models.Model):
    name            = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class UserItemCondition(models.Model):
    name            = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class UserItem(models.Model):
    name            = models.CharField(max_length=200)
    slug            = models.SlugField()
    description     = models.TextField()
    image_url       = models.CharField(max_length=200)
    category        = models.ForeignKey(UserItemCategory, on_delete=models.PROTECT)
    condition       = models.ForeignKey(UserItemCondition, on_delete=models.PROTECT)
    replacement_cost = models.FloatField()
    owner           = models.ForeignKey(User, on_delete=models.PROTECT, related_name='items')
    item_status     = models.ForeignKey(UserItemStatus, on_delete=models.PROTECT)

    def __str__(self):
        return self.category.name + ': ' + self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(UserItem, self).save(*args, **kwargs)

class UserItemCheckout(models.Model):
    user_item       = models.ForeignKey(UserItem, on_delete=models.PROTECT, related_name='item_history')
    checkout_status = models.ForeignKey(CheckoutStatus, on_delete=models.PROTECT)
    reason          = models.CharField(max_length=200, blank=True, null=True)
    request_date    = models.DateTimeField()
    checkout_date   = models.DateTimeField(blank=True, null=True)
    checkin_date    = models.DateTimeField(blank=True, null=True)
    borrower        = models.ForeignKey(User, on_delete=models.PROTECT, related_name='checkouts')
    due_date        = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user_item.name
