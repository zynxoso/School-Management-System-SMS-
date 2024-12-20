from django import template

register = template.Library()

@register.filter
def percentage(value, max_value):
    try:
        return round((float(value) / float(max_value)) * 100, 1)
    except (ValueError, ZeroDivisionError, TypeError):
        return 0.0

@register.filter
def grade_class(percentage):
    try:
        percentage = float(percentage)
        if percentage >= 90:
            return 'bg-success'
        elif percentage >= 80:
            return 'bg-info'
        elif percentage >= 70:
            return 'bg-primary'
        elif percentage >= 60:
            return 'bg-warning'
        else:
            return 'bg-danger'
    except (ValueError, TypeError):
        return 'bg-secondary'
