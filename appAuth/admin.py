from django.contrib import admin

# Register your models here.
from .models import UserInfo, Company, Credit_card
admin.site.register(UserInfo)
admin.site.register(Company)
admin.site.register(Credit_card)