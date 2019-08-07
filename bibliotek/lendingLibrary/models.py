from django.db import models

class User(models.Model):
    name            = models.CharField(max_length=200)
    email           = models.CharField(max_length=200)
    phone_number    = models.CharField(max_length=200)

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
    type            = models.ForeignKey(UserItemCategory, on_delete=models.CASCADE)
    condition       = models.ForeignKey(UserItemCondition, on_delete=models.CASCADE)
    replacement_cost = models.DecimalField(max_digits=6, decimal_places=2)
    owner           = models.ForeignKey(User, on_delete=models.CASCADE)
    checked_out     = models.BooleanField()
    hidden          = models.BooleanField()

    def __str__(self):
        return self.name

class UserItemCheckout(models.Model):
    user_item       = models.ForeignKey(UserItem, on_delete=models.CASCADE)
    status          = models.ForeignKey(CheckoutStatus, on_delete=models.CASCADE)
    request_date    = models.DateTimeField()
    checkout_date   = models.DateTimeField(default=None, blank=True, null=True)
    checkin_date    = models.DateTimeField(default=None, blank=True, null=True)
    borrower        = models.ForeignKey(User, on_delete=models.CASCADE)
    due_date        = models.DateTimeField(default=None, blank=True, null=True)

    def __str__(self):
        return self.user_item.name
