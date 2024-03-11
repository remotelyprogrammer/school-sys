from django.urls import path
from . import views
from .views import EnrollmentHomeView

app_name = 'enrollment'

urlpatterns = [
    path('', EnrollmentHomeView.as_view(), name='enrollment-home'),
    path('create/', views.CreateEnrollmentView.as_view(), name='enrollment-create'),

]