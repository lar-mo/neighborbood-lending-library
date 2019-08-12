from django.contrib import admin

from .models import UserItemStatus
from .models import CheckoutStatus
from .models import CheckoutStatusReason
from .models import UserItemCategory
from .models import UserItemCondition
from .models import UserItem
from .models import UserItemCheckout

admin.site.register(UserItemStatus)
admin.site.register(CheckoutStatus)
admin.site.register(CheckoutStatusReason)
admin.site.register(UserItemCategory)
admin.site.register(UserItemCondition)
admin.site.register(UserItem)
admin.site.register(UserItemCheckout)
