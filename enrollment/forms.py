from django import forms
from .models import Enrollment, Subject, GradeLevel, Curriculum
from django.forms import inlineformset_factory


from dal import autocomplete


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ('student', 'school_year', 'grade_level', 'enrollment_date')
        widgets = {
        'student':autocomplete.ModelSelect2(url='enrollment:student-autocomplete'),
        }



class CurriculumForm(forms.ModelForm):
    class Meta:
        model = Curriculum
        fields = ['curriculum_name']

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['code', 'name', 'description', 'curriculum']


SubjectInlineFormSet = inlineformset_factory(
    Curriculum,  # The parent model
    Subject,  # The child model
    form=SubjectForm,
    extra=2,  # How many blank forms you want to display
    can_delete=True  # Allows deletion of subjects
)