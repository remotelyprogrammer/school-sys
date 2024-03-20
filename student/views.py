from django.shortcuts import render, redirect, get_object_or_404
from .models import Contact, Student, Address
from django.views.generic.edit import CreateView, DeleteView
from .forms import StudentForm, ContactFormSet, AddressForm, AddressFormSet, ContactForm, AddressForm
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views import View


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'student/student-confirm-delete.html'
    success_url = reverse_lazy('student:student-list')

    def post(self, request, *args, **kwargs):
        student = self.get_object()
        if student.status == 'active':
            # Return an error message and prevent deletion
            return HttpResponseForbidden('This student cannot be deleted because they are still in active status.')
        else:
            return super(StudentDeleteView, self).post(request, *args, **kwargs)

class StudentListView(ListView):
    model = Student
    template_name = 'student/student-list.html'
    context_object_name = 'students'

class StudentDetailView(DetailView):
    model = Student
    template_name = 'student/student-detail.html'
    context_object_name = 'student'

    def get_context_data(self, **kwargs):
        context = super(StudentDetailView, self).get_context_data(**kwargs)
        # Safely get the student's address if it exists, otherwise set it to None
        try:
            context['address'] = self.object.address
        except Student.address.RelatedObjectDoesNotExist:
            context['address'] = None

        # Add the student's contacts to the context
        context['contacts'] = self.object.contacts.all() if hasattr(self.object, 'contacts') else []
        return context


class CreateStudentView(View):
    template_name = 'student/create-student.html'

    def get(self, request, *args, **kwargs):
        form = StudentForm()
        address_form = AddressForm()
        contact_form = ContactForm()
        return render(request, self.template_name, {
            'form': form,
            'address_form': address_form,
            'contact_form': contact_form,
        })

    def post(self, request, *args, **kwargs):
        form = StudentForm(request.POST)
        address_form = AddressForm(request.POST)
        contact_form = ContactForm(request.POST)

        if form.is_valid() and address_form.is_valid() and contact_form.is_valid():
            student = form.save()
            address = address_form.save(commit=False)
            address.student = student
            address.save()
            contact = contact_form.save(commit=False)
            contact.student = student
            contact.save()

            return redirect('student:student-list')  # Adjust the redirect to where you need.
        
        return render(request, self.template_name, {
            'form': form,
            'address_formset': address_form,
            'contact_formset': contact_form,
        })
        
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