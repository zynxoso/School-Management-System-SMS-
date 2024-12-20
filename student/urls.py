from django.urls import path
from . import views

app_name = 'student'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('students/', views.StudentListView.as_view(), name='student_list'),
    path('student/add/', views.StudentCreateView.as_view(), name='student_create'),
    path('student/<int:pk>/', views.StudentDetailView.as_view(), name='student_detail'),
    path('student/<int:pk>/edit/', views.StudentUpdateView.as_view(), name='student_update'),
    path('student/<int:pk>/delete/', views.StudentDeleteView.as_view(), name='student_delete'),
    path('student/<int:pk>/profile/', views.StudentProfileView.as_view(), name='student_profile'),
]
