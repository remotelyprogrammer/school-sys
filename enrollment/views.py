from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from .models import Enrollment
from .forms import EnrollmentForm


class EnrollmentHomeView(TemplateView):
	template_name = 'enrollment/enrollment-home.html'


class CreateEnrollmentView(CreateView):
	model = Enrollment
	template_name = 'enrollment/create-enrollment.html'
	form_class = EnrollmentForm

