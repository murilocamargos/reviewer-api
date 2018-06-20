from django.contrib import admin

from review.models import Company, Review


class ReviewAdmin(admin.ModelAdmin):
    readonly_fields = ('title', 'company', 'reviewer', 'ip_address', 'rating',\
        'created_at', 'summary',)
    list_display = ('title', 'reviewer', 'company', 'rating', 'created_at')

admin.site.register(Company)
admin.site.register(Review, ReviewAdmin)
