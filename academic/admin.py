from django.contrib import admin
from django.utils.html import format_html
from .models import (
    AcademicYear, Class, Subject, ClassSubject,
    StudentEnrollment, Attendance, Grade
)

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'section', 'academic_year', 'class_teacher', 'capacity')
    list_filter = ('academic_year', 'section')
    search_fields = ('name', 'section', 'class_teacher__username')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'credits', 'get_actions')
    search_fields = ('name', 'code')
    
    def get_actions(self, obj):
        return format_html(
            '<a class="button" href="{}/change/"><i class="fas fa-edit"></i> Edit</a>&nbsp;'
            '<a class="button" href="{}/delete/"><i class="fas fa-trash"></i> Delete</a>',
            obj.id, obj.id
        )
    get_actions.short_description = 'Actions'
    
    class Media:
        css = {
            'all': [
                'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css',
                'admin/css/custom_admin.css'
            ]
        }

@admin.register(ClassSubject)
class ClassSubjectAdmin(admin.ModelAdmin):
    list_display = ('subject', 'class_group', 'teacher')
    list_filter = ('class_group__academic_year', 'subject')
    search_fields = ('subject__name', 'teacher__username')

@admin.register(StudentEnrollment)
class StudentEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_group', 'enrollment_date', 'status')
    list_filter = ('status', 'class_group__academic_year')
    search_fields = ('student__username', 'class_group__name')
    date_hierarchy = 'enrollment_date'

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_subject', 'date', 'status')
    list_filter = ('status', 'date', 'class_subject')
    search_fields = ('student__username', 'class_subject__subject__name')
    date_hierarchy = 'date'

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_subject', 'assessment_type', 'score', 'max_score', 'percentage', 'date')
    list_filter = ('assessment_type', 'class_subject', 'date')
    search_fields = ('student__username', 'class_subject__subject__name')
    date_hierarchy = 'date'
