from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, FormView, ListView, DetailView

from courses.utils import get_view_at_console1
from courses.models import Course
from students.forms import CourseEnrollForm


class StudentRegistrationView(CreateView):
    template_name = 'students/student/registration.html'
    success_url = reverse_lazy('students:student_course_list')
    form_class = UserCreationForm

    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        kwargs_for_authenticate = {
            'request': self.request,
            'username': cd['username'],
            'password': cd['password1'],
        }
        user = authenticate(**kwargs_for_authenticate)
        login(self.request, user)
        return result


class SrudentEnrollCourseView(LoginRequiredMixin, FormView):
    form_class = CourseEnrollForm
    course = None

    def form_valid(self, form):
        self.course = form.cleaned_data.get('course')
        if isinstance(self.course, Course):
            self.course.students.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('students:student_course_detail', args=[self.course.pk])


class StudentCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'students/course/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user, ])


# @cache_page(60 * 5)
class StudentCourseDetailView(DetailView):
    model = Course
    template_name = 'students/course/detail.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user, ])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        # в этом self.kwargs (не kwargs передаваемый в get_context_data)
        # лежат наши url параметры (тупо, да)
        if 'module_id' in self.kwargs:
            context['module'] = course.modules.get(pk=self.kwargs['module_id'])
        else:
            context['module'] = course.modules.first()
        get_view_at_console1(context['module'])
        return context
