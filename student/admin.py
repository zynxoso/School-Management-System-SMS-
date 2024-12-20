from django.contrib import admin
from .models import Student

# Register your models here.

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'get_full_name', 'grade_level', 'section', 'gender', 'is_active')
    list_filter = ('grade_level', 'section', 'gender', 'is_active', 'nationality', 'blood_group')
    search_fields = ('student_id', 'first_name', 'last_name', 'email', 'phone_number')
    
    fieldsets = (
        ('Personal Information', {
            'fields': (
                ('student_id', 'is_active'),
                ('first_name', 'middle_name', 'last_name'),
                ('date_of_birth', 'gender'),
                ('blood_group', 'religion'),
                'nationality',
                ('email', 'phone_number'),
            )
        }),
        ('Academic Information', {
            'fields': (
                ('grade_level', 'section'),
                'previous_school',
                'academic_year'
            )
        }),
        ('Contact Information', {
            'fields': (
                'address',
                ('city', 'state', 'postal_code')
            )
        }),
        ('Emergency Contact', {
            'fields': (
                'emergency_contact_name',
                'emergency_contact_relationship',
                'emergency_contact_phone'
            )
        }),
        ('Father Information', {
            'fields': (
                'father_name',
                'father_occupation',
                ('father_phone', 'father_email')
            ),
            'classes': ('collapse',)
        }),
        ('Mother Information', {
            'fields': (
                'mother_name',
                'mother_occupation',
                ('mother_phone', 'mother_email')
            ),
            'classes': ('collapse',)
        }),
        ('Guardian Information', {
            'fields': (
                'guardian_name',
                'guardian_relationship',
                ('guardian_phone', 'guardian_email')
            ),
            'classes': ('collapse',)
        }),
        ('Medical Information', {
            'fields': (
                'medical_conditions',
                'allergies',
                'medications'
            ),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ('created_at', 'updated_at')
