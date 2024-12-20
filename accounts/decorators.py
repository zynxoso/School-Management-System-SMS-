from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'Please log in to access this page.')
                return redirect('login')
            
            if request.user.user_type not in allowed_roles:
                messages.error(request, 'You do not have permission to access this page.')
                
                # Redirect based on user type
                if request.user.user_type == 'teacher':
                    return redirect('academic:teacher_classes')
                elif request.user.user_type == 'student':
                    return redirect('student:dashboard')
                elif request.user.user_type == 'parent':
                    return redirect('academic:children_list')
                else:
                    return redirect('student:dashboard')
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
