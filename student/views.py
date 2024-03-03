from django.shortcuts import render, redirect, get_object_or_404
from .models import Contact, Student, Address
from django.views.generic.edit import CreateView
from .forms import StudentForm, ContactFormSet, AddressForm, AddressFormSet
from django.urls import reverse_lazy


# class CreateStudentView(CreateView):
#         model = Student
#         form_class = StudentForm
#         # fields = ['std_sch_id','first_name', 'middle_name','last_name','suffix','birth_date', 'nationality', 'civil_status','sex',
#         #           'religion', 'mobile_number', 'telephone_number', 'personal_email'
#         #           ]
#         template_name = 'student/create-student.html'
#         context_object_name = 'student'
#         success_url = reverse_lazy('student:student-home')

class CreateStudentView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'student/create-student.html'
    success_url = reverse_lazy('student:student-home')

    def get_context_data(self, **kwargs):
        context = super(CreateStudentView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['contact_formset'] = ContactFormSet(self.request.POST)
            context['address_formset'] = AddressFormSet(self.request.POST)
        else:
            context['contact_formset'] = ContactFormSet()
            context['address_formset'] = AddressFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        address_formset = context['address_formset']
        contact_formset = context['contact_formset']
        if form.is_valid() and address_formset.is_valid() and contact_formset.is_valid():
            self.object = form.save()
            address_formset.instance = self.object
            address_formset.save()
            contact_formset.instance = self.object
            contact_formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))
        
def home(request):
    return render(request, 'student/base.html')

def add_student_contacts(request, pk): #adding contact to a defined pk/student id
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        formset = ContactFormSet(request.POST, instance=student)
        if formset.is_valid():
            formset.save()
            return redirect('student:student-home')  # Replace with your desired redirect
    else:
        formset = ContactFormSet(instance=student)
    return render(request, 'student/add-contacts.html', {'formset': formset, 'student': student})