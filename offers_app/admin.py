from django.contrib import admin

from .models import Offer, OfferDetail


class OfferDetailInline(admin.TabularInline):
    model = OfferDetail
    extra = 0
    min_num = 1
    fields = (
        'offer_type',
        'title',
        'price',
        'delivery_time_in_days',
        'revisions',
        'features',
    )


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'user',
        'detail_count',
        'created_at',
        'updated_at',
    )
    list_filter = (
        'created_at',
        'updated_at',
    )
    search_fields = (
        'title',
        'description',
        'user__username',
        'user__email',
    )
    readonly_fields = (
        'created_at',
        'updated_at',
    )
    fieldsets = (
        ('Angebot', {
            'fields': (
                'user',
                'title',
                'image',
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
    inlines = (OfferDetailInline,)
    autocomplete_fields = ('user',)
    date_hierarchy = 'updated_at'

    @admin.display(description='Pakete')
    def detail_count(self, obj):
        return obj.details.count()


@admin.register(OfferDetail)
class OfferDetailAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'offer',
        'offer_type',
        'price',
        'delivery_time_in_days',
        'revisions',
    )
    list_filter = (
        'offer_type',
        'delivery_time_in_days',
    )
    search_fields = (
        'title',
        'offer__title',
        'offer__user__username',
        'offer__user__email',
    )
    autocomplete_fields = ('offer',)
