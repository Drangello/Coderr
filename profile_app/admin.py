from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    extra = 0
    fields = (
        'type',
        'first_name',
        'last_name',
        'file',
        'location',
        'tel',
        'working_hours',
        'description',
    )


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_active',
    )
    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name',
        'profile__first_name',
        'profile__last_name',
    )
    list_filter = (
        'is_staff',
        'is_active',
        'profile__type',
    )

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj == request.user:
            return False
        return super().has_delete_permission(request, obj)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'first_name',
        'last_name',
        'type',
        'location',
        'tel',
        'created_at',
    )
    list_filter = (
        'type',
        'created_at',
    )
    search_fields = (
        'user__username',
        'user__email',
        'first_name',
        'last_name',
        'location',
        'tel',
    )
    readonly_fields = ('created_at',)
    autocomplete_fields = ('user',)
    fieldsets = (
        ('Benutzer', {
            'fields': (
                'user',
                'type',
            ),
        }),
        ('Profil-Daten', {
            'fields': (
                'first_name',
                'last_name',
                'file',
                'location',
                'tel',
                'working_hours',
                'description',
            ),
        }),
        ('Zeitstempel', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
