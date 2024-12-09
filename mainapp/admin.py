from django.contrib import admin

from mainapp.models import MyUser


@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    pass
# Register your models here.


