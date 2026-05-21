from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'customer_user',
        'business_user',
        'status',
        'price',
        'delivery_time_in_days',
        'updated_at',
    )
    list_filter = (
        'status',
        'offer_type',
        'created_at',
        'updated_at',
    )
    search_fields = (
        'title',
        'customer_user__username',
        'customer_user__email',
        'business_user__username',
        'business_user__email',
    )
    readonly_fields = (
        'created_at',
        'updated_at',
    )
    autocomplete_fields = (
        'customer_user',
        'business_user',
    )
    date_hierarchy = 'updated_at'
    fieldsets = (
        ('Auftrag', {
            'fields': (
                'title',
                'status',
                'customer_user',
                'business_user',
            ),
        }),
        ('Paket-Daten', {
            'fields': (
                'offer_type',
                'price',
                'delivery_time_in_days',
                'revisions',
                'features',
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
