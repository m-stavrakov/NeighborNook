from django.contrib import admin
from .models import Profile

class MemberAdmin(admin.ModelAdmin):
    list_display = ('get_first_name', 'get_last_name', 'user', 'profile_img')
    search_fields = ('user__first_name', 'user__last_name, user__username')

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = 'First Name'
    get_first_name.admin_order_field = 'user__first_name'

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.short_description = 'Last Name'
    get_last_name.admin_order_field = 'user__last_name'

admin.site.register(Profile, MemberAdmin)