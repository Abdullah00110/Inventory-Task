from django.contrib import admin
from authentication.models import MyUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserModelAdmin(BaseUserAdmin):
    # Fields to display in the admin panel list view
    list_display = ('id', 'username', 'email', 'is_admin')

    # Fields to filter the users
    list_filter = ('is_active', 'is_admin')

    # Fieldsets for organizing the fields in the admin panel
    fieldsets = (
        ('User Credentials', {'fields': ('username', 'email', 'password')}),  # Username, Email, and Password login
        ('Personal info', {'fields': ('name', 'tc')}),  # User's name and terms and conditions acceptance
        ('Permissions', {'fields': ('is_admin', 'is_active')}),  # Admin and active status management
    )

    # Fields to display when adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'tc', 'password', 'password2'),  # Password fields for user creation
        }),
    )

    # Enable search by username and email, and ordering by email, id
    search_fields = ('username', 'email')
    ordering = ('email', 'id')
    filter_horizontal = ()  # Not using any horizontal filter fields

# Register the customized user admin
admin.site.register(MyUser, UserModelAdmin)
