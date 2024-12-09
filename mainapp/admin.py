from django.contrib import admin

from mainapp.models import MyUser, AdminRule


@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    pass
# Register your models here.


@admin.register(AdminRule)
class AdminRuleAdmin(admin.ModelAdmin):
    pass
