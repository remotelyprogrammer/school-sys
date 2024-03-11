from django import forms
from .models import Enrollment


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'school_year', 'grade_level', 'enrollment_date']