from django.shortcuts import render
from django.views.generic.base import TemplateView

class EnrollmentHomeView(TemplateView):
	template_name = 'enrollment/enrollment-home.html'
