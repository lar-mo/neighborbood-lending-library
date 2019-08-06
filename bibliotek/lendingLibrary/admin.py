from django.contrib import admin

from .models import User
from .models import UserItem
from .models import UserItemCheckout
from .models import CheckoutStatus
from .models import UserItemCategory

admin.site.register(User)
admin.site.register(UserItem)
admin.site.register(UserItemCheckout)
admin.site.register(CheckoutStatus)
admin.site.register(UserItemCategory)
