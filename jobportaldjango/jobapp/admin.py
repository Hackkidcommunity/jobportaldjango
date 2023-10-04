from django.contrib import admin
from . models import *
@admin.action(description="Mark selected employers as verified")
def mark_verified(modeladmin, request, queryset):
    queryset.update(is_verified=True)
@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_verified_display']  # Add 'is_verified_display' to list_display

    def is_verified_display(self, obj):
        # Customize the display of 'is_verified' field
        if obj.is_verified:
            return 'Verified ✅'
        else:
            return 'Not Verified ❌'

    is_verified_display.short_description = 'Verification Status'
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'is_verified',)  # Add 'is_verified' to the list display
    actions = [mark_verified]  # Add the custom admin action    
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'application_count')
    readonly_fields = ('application_count',)

    def application_count(self, obj):
        return obj.jobapplication_set.count()

    application_count.short_description = 'Application Count'
admin.site.register(Application)
admin.site.register(Admin)
