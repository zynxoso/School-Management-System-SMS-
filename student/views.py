from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Count, Q
from .models import Student
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'student_id', 'first_name', 'middle_name', 'last_name', 'date_of_birth',
            'gender', 'blood_group', 'religion', 'nationality', 'email', 'phone_number',
            'grade_level', 'section', 'academic_year', 'previous_school',
            'address', 'city', 'state', 'postal_code',
            'emergency_contact_name', 'emergency_contact_relationship', 'emergency_contact_phone',
            'father_name', 'father_occupation', 'father_phone', 'father_email',
            'mother_name', 'mother_occupation', 'mother_phone', 'mother_email',
            'guardian_name', 'guardian_relationship', 'guardian_phone', 'guardian_email',
            'medical_conditions', 'allergies', 'medications', 'is_active'
        ]
        widgets = {
            'student_id': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'blood_group': forms.Select(attrs={'class': 'form-select'}),
            'religion': forms.Select(attrs={'class': 'form-select'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'grade_level': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'section': forms.TextInput(attrs={'class': 'form-control'}),
            'academic_year': forms.Select(attrs={'class': 'form-select'}),
            'previous_school': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_relationship': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'father_occupation': forms.TextInput(attrs={'class': 'form-control'}),
            'father_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'father_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_occupation': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'guardian_name': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_relationship': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'medical_conditions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'allergies': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'medications': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

class DashboardView(TemplateView):
    template_name = 'student/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_students'] = Student.objects.count()
        context['active_students'] = Student.objects.filter(is_active=True).count()
        context['grade_levels'] = Student.objects.values('grade_level').distinct().count()
        context['sections'] = Student.objects.values('section').distinct().count()
        context['recent_students'] = Student.objects.order_by('-created_at')[:5]

        # Calculate grade distribution
        total_students = context['total_students']
        grade_counts = Student.objects.values('grade_level').annotate(count=Count('id'))
        context['grade_distribution'] = {
            grade['grade_level']: {
                'count': grade['count'],
                'percentage': (grade['count'] / total_students * 100) if total_students > 0 else 0
            }
            for grade in grade_counts
        }

        return context

class StudentListView(ListView):
    model = Student
    template_name = 'student/student_list.html'
    context_object_name = 'students'
    paginate_by = 10

    def get_queryset(self):
        try:
            queryset = Student.objects.all()
            print(f"Debug: Initial queryset count: {queryset.count()}")
            
            search = self.request.GET.get('search')
            grade = self.request.GET.get('grade')
            section = self.request.GET.get('section')
            status = self.request.GET.get('status')

            if search:
                queryset = queryset.filter(
                    Q(student_id__icontains=search) |
                    Q(first_name__icontains=search) |
                    Q(last_name__icontains=search) |
                    Q(email__icontains=search)
                )
            if grade:
                queryset = queryset.filter(grade_level=grade)
            if section:
                queryset = queryset.filter(section=section)
            if status:
                is_active = status == 'active'
                queryset = queryset.filter(is_active=is_active)

            final_queryset = queryset.order_by('grade_level', 'last_name', 'first_name')
            print(f"Debug: Final queryset count: {final_queryset.count()}")
            print(f"Debug: Final queryset SQL: {final_queryset.query}")
            return final_queryset
        except Exception as e:
            print(f"Debug: Error in get_queryset: {str(e)}")
            return Student.objects.none()

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            print("Debug: get_context_data called")
            print(f"Debug: Context keys: {context.keys()}")
            print(f"Debug: Students in context: {len(context.get('students', []))}")
            print(f"Debug: Page obj: {context.get('page_obj')}")
            
            context['grade_choices'] = Student.objects.values_list(
                'grade_level', flat=True).distinct().order_by('grade_level')
            context['section_choices'] = Student.objects.values_list(
                'section', flat=True).distinct().order_by('section')
            
            return context
        except Exception as e:
            print(f"Debug: Error in get_context_data: {str(e)}")
            return super().get_context_data(**kwargs)

class StudentDetailView(DetailView):
    model = Student
    template_name = 'student/student_detail.html'
    context_object_name = 'student'

class StudentProfileView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'student/student_profile.html'
    context_object_name = 'student'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.get_object()
        context['page_title'] = f"Student Profile - {student.get_full_name()}"
        return context

class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'student/student_form.html'
    success_url = reverse_lazy('student:student_list')

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, 'Student was created successfully.')
            return response
        except Exception as e:
            messages.error(self.request, f'Error creating student: {str(e)}')
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'student/student_form.html'
    success_url = reverse_lazy('student:student_list')

    def form_valid(self, form):
        messages.success(self.request, 'Student was updated successfully.')
        return super().form_valid(form)

class StudentDeleteView(DeleteView):
    model = Student
    success_url = reverse_lazy('student:student_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Student was deleted successfully.')
        return super().delete(request, *args, **kwargs)
