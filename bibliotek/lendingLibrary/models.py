from django.db import models
from django.contrib.auth.models import User

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
    description     = models.TextField(default="add some detail")
    image_url       = models.CharField(default="https://lar-mo.com/images/lazy_placeholder.gif", max_length=200)
    type            = models.ForeignKey(UserItemCategory, on_delete=models.PROTECT)
    condition       = models.ForeignKey(UserItemCondition, on_delete=models.PROTECT)
    replacement_cost = models.FloatField()
    owner           = models.ForeignKey(User, on_delete=models.PROTECT, related_name='items')
    item_status     = models.ForeignKey(UserItemStatus, on_delete=models.PROTECT)

    def __str__(self):
        return self.type.name + ': ' + self.name

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
