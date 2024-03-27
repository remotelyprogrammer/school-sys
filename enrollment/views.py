from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from .models import Enrollment, SchoolYear, Subject, Curriculum, GradeLevel
from .forms import EnrollmentForm, SubjectForm, CurriculumForm, SubjectInlineFormSet
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView


class EnrollmentHomeView(TemplateView):
	template_name = 'enrollment/enrollment-home.html'


from dal import autocomplete
from student.models import Student

class EnrollmentAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Student.objects.all()

        if self.q:
            qs = qs.filter(first_name__istartswith=self.q)

        print(qs)
        return qs


class CreateEnrollmentView(CreateView):
    model = Enrollment
    template_name = 'enrollment/create-enrollment.html'
    form_class = EnrollmentForm
    success_url = reverse_lazy('enrollment:enrollment-home')  # Adjust this to where you want to redirect after success

    def form_valid(self, form):
        # Check if the student is already enrolled in the selected school year
        student = form.cleaned_data['student']
        school_year = form.cleaned_data['school_year']
        enrollment_exists = Enrollment.objects.filter(student=student, school_year=school_year).exists()

        if enrollment_exists:
            # If the student is already enrolled in this school year, show an error message
            form.add_error(None, 'This student is already enrolled in the selected school year.')
            return self.form_invalid(form)

        # If the check passes, proceed with the normal form handling, which saves the Enrollment
        return super().form_valid(form)

    def form_invalid(self, form):
        # If the form is invalid, return to the same page with error messages
        return self.render_to_response(self.get_context_data(form=form))


class EnrollmentDetailView(DetailView):
    model = Enrollment
    template_name = 'enrollment/enrollee-detail.html'
    context_object_name = 'enrollee'

    def get_context_data(self, **kwargs):
        context = super(EnrollmentDetailView, self).get_context_data(**kwargs)
        

        # context['enrollment'] = self.object.enrollment.all() if hasattr(self.object, 'enrollments') else []
        return context


class EnrollmentListView(ListView):
    model = Enrollment
    template_name = 'enrollment/enrollment-list.html'
    context_object_name = 'enrollees'


class CreateSchoolYearView(CreateView):
    model = SchoolYear
    template_name = 'enrollment/create-school-year.html'
    success_url = reverse_lazy('enrollment:enrollment-home')
    fields = ['start_year', 'end_year', 'is_current']


class SchoolYearDetailView(DetailView):
    model = SchoolYear
    template_name = 'enrollment/school-year-details.html'
    context_object_name = 'school_year'


class SchoolYearListView(ListView):
    model = SchoolYear
    template_name = 'enrollment/school-year-list.html'
    context_object_name = 'school_years'


class SubjectListView(ListView):
    model = Subject
    template_name = 'enrollment/subject-list.html'
    context_object_name = 'subjects'

class SubjectCreateView(CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'enrollment/subject-create.html'
    success_url = reverse_lazy('enrollment:subject-list')


class CurriculumCreateView(CreateView):
    model = Curriculum
    template_name = 'enrollment/curriculum-create.html'
    success_url = reverse_lazy('enrollment:subject-list')
    fields = '__all__'

class CurriculumListView(ListView):
    model = Curriculum
    template_name = 'enrollment/curriculum-list.html'
    context_object_name = 'curricula'

def curriculumset_create_or_update(request, curriculum_id=None):
    if curriculum_id:
        curriculum = Curriculum.objects.get(pk=curriculum_id)
    else:
        curriculum = Curriculum()

    if request.method == 'POST':
        form = CurriculumForm(request.POST, instance=curriculum)
        formset = SubjectInlineFormSet(request.POST, instance=curriculum)
        
        if form.is_valid() and formset.is_valid():
            created_curriculum = form.save()
            formset.instance = created_curriculum
            formset.save()
            return redirect('enrollment:curriculumset-list')
    else:
        form = CurriculumForm(instance=curriculum)
        formset = SubjectInlineFormSet(instance=curriculum)
    
    return render(request, 'enrollment/curriculumset-create.html', {'form': form, 'formset': formset})


class GradeLevelCreateView(CreateView):
    model = GradeLevel
    template_name = 'enrollment/create-grade-level.html'
    success_url = reverse_lazy('enrollment:subject-list')
    fields = ['name', 'order']


class GradeLevelListView(ListView):
    model = GradeLevel
    template_name = 'enrollment/grade-level-list.html'
    context_object_name = 'grade_levels'