from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from .models import Enrollment
from .forms import EnrollmentForm


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
