from django.contrib import admin
from .models import Recipe, UserQuery

admin.site.register(Recipe)

@admin.register(UserQuery)
class UserQueryAdmin(admin.ModelAdmin):
    list_display = ('query_text', 'chat_id', 'created_at')
    readonly_fields = ('query_text', 'chat_id', 'created_at')