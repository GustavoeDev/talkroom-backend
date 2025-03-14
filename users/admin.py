from django.contrib import admin
from users.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'avatar', 'is_superuser', 'last_login')