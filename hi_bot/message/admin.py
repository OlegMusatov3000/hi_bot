from django.contrib import admin

from .models import User, Messages


@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipient', 'created')
    search_fields = ('recipient',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'role')
    search_fields = ('username',)
    list_filter = ('role',)
