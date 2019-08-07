from django.contrib import admin

from .models import UserItem
from .models import UserItemCheckout
from .models import UserItemStatus
from .models import UserItemCategory
from .models import UserItemCondition

admin.site.register(UserItem)
admin.site.register(UserItemCheckout)
admin.site.register(UserItemStatus)
admin.site.register(UserItemCategory)
admin.site.register(UserItemCondition)
