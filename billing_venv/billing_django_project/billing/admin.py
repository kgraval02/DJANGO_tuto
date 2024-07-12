from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at', 'reviewed')
    list_filter = ('reviewed', 'created_at')
    search_fields = ('user__username', 'message')


admin.site.register(Feedback, FeedbackAdmin)
