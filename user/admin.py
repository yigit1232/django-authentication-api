from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Recovery

admin.site.register(Recovery)

@admin.register(User)
class Admin(UserAdmin):
    list_display = ('username','name','email','is_active','is_staff')
    list_filter = ('is_staff','is_active')
    search_fields = ['username']
    class Meta:
        model = User