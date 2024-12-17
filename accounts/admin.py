from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, TeacherProfile, StudentProfile, ParentProfile

class TeacherProfileInline(admin.StackedInline):
    model = TeacherProfile
    can_delete = False
    verbose_name_plural = 'Teacher Profile'

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_active')
    list_filter = ('user_type', 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'address', 'date_of_birth', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_type')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'user_type', 'email', 'first_name', 'last_name'),
        }),
    )
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

    def get_inlines(self, request, obj=None):
        if obj is None:
            return []
        if obj.user_type == 'teacher':
            return [TeacherProfileInline]
        return []

@admin.register(User)
class UserAdmin(CustomUserAdmin):
    pass

@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'department', 'qualification', 'joining_date')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'employee_id', 'department')
    list_filter = ('department', 'joining_date')
