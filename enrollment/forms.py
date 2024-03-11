from django import forms
from .models import Enrollment


from dal import autocomplete


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ('student', 'school_year', 'grade_level', 'enrollment_date')
        widgets = {
        'student':autocomplete.ModelSelect2(url='enrollment:student-autocomplete'),
        }