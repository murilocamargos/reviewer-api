from django.contrib import admin


class SoftDeletionModelAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        """
        For django admin, shows every object, even deleted ones.
        """
        return self.model.all_objects.all().order_by('deleted_at')

    def get_list_display(self, request):
        """
        Create a column on django admin object listing.
        """
        return list(self.list_display) + ['enabled']

    def enabled(self, obj):
        return obj.deleted_at is None
    enabled.boolean = True
    enabled.admin_order_field = 'deleted_at'
