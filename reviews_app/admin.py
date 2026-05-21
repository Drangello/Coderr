from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'business_user',
        'reviewer',
        'rating',
        'updated_at',
    )
    list_filter = (
        'rating',
        'created_at',
        'updated_at',
    )
    search_fields = (
        'business_user__username',
        'business_user__email',
        'reviewer__username',
        'reviewer__email',
        'description',
    )
    readonly_fields = (
        'created_at',
        'updated_at',
    )
    autocomplete_fields = (
        'business_user',
        'reviewer',
    )
    date_hierarchy = 'updated_at'
    fieldsets = (
        ('Bewertung', {
            'fields': (
                'business_user',
                'reviewer',
                'rating',
                'description',
            ),
        }),
        ('Zeitstempel', {
            'fields': (
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',),
        }),
    )
