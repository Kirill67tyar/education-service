from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.base import View, TemplateResponseMixin
from django.views.generic.edit import (CreateView, UpdateView, DeleteView, ModelFormMixin)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from courses.forms import ModuleFormSet
from courses.utils import get_view_at_console1
from courses.models import (Subject, Course, Module, Content)


def experiments_view(request):
    get_view_at_console1(request.session)
    return JsonResponse({'status': 'ok', })


# недействительный обработчик*****************************
class OldManageCourseListView(ListView):
    model = Course
    template_name = 'courses/manage/course/list.html'

    def get_queryset(self):
        qs = super(OldManageCourseListView, self).get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerMixin:

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin:

    def form_valid(self, form):
        # вот благодаря этой строчке наши курсы автоматически сохраняются за нужным юзером
        # я сделал здесь try - except потому что у обычных форм атрибута instance может и не быть
        # вроде как он есть только у ModelForm
        try:
            form.instance.owner = self.request.user
        except AttributeError:
            pass
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview', ]  # скорее всего здесь для LoginRequiredMixin
    success_url = reverse_lazy('courses:manage_course_list')  # скорее всего здесь для LoginRequiredMixin


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    fields = ['subject', 'title', 'slug', 'overview', ]
    template_name = 'courses/manage/course/form.html'
    success_url = reverse_lazy('courses:manage_course_list')


class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/manage/course/list.html'


class CourseCreateView(PermissionRequiredMixin, OwnerCourseEditMixin, CreateView):
    permission_required = 'courses.add_course'


class CourseUpdateView(PermissionRequiredMixin, OwnerCourseEditMixin, UpdateView):
    permission_required = 'courses.change_course'


class CourseDeleteView(PermissionRequiredMixin, OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'
    success_url = reverse_lazy('courses:manage_course_list')
    permission_required = 'courses.delete_course'


class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/manage/course/formset.html'
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        self.course = get_object_or_404(klass=Course, pk=pk, owner=request.user)
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'formset': formset, 'course': self.course, })

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect(reverse('courses:manage_course_list'))
        return self.render_to_response({'formset': formset, 'course': self.course, })


"""
CourseModuleUpdateView 
унаследован от: TemplateResponseMixin View

TemplateResponseMixin - примесь, которая добавит формирование HTML шаблона
и вернет его в качестве ответа на запрос.
Использует шаблон template_name определенный как атрибут класса. 
Добавляет в дочерние классы метод render_to_response
в который можно просто передать контекст и он будет использовать template_name атрибута класса

View - базовый класс для обработчиков Django

get_formset - здесь для того, чтобы избежать дублирование кода

dispatch
метода, который определен в базовом классе View.
Принимает объект запроса (request) и его параметры
и пытается вызвать метод в python коде, который соответствует методу HTTP запроса
Если запрос отправлен с методом GET то вызовет метод get() в класса
Если POST - то post()

get

post
"""

"""
Примиси (Mixins) - это класс, который используется при множественном наследовании.
При определении класса можно задействовать несколько примесей, каждая из которых добавит
часть функций в класс.
Примеси удобны в двух случаях:
1 - нужно использовать несколько различных функций в рамках моего класса
2 - реализовать одну и туже функциональность в нескольких классах

В rest_framework тоже используются миксины для CRUD функционала
Вспомни, миксины в rest_framework добавляют нам функционал list, retrieve,create, update, partial_update, destroy
И работают они совместно с GenericApiView

Чтобы определять самому миксины - нужно хорошо разбираться в django, какие методы, за что отвечают,
какие вызываются и когда, какие атрибуты используются.

*****Разбор классов обработчиков, и логики кастомных миксинов*****

OwnerMixin
базовый миксин для работы owner.

OwnerEditMixin - для CreateView и UpdateView (переопределяем form_valid), для работы с owner

OwnerCourseMixin 
унаследован от - OwnerMixin, LoginRequiredMixin
класс для работы с курсом. будет использоваться для функционала Read и Delete

OwnerCourseEditMixin 
унаследован от - OwnerCourseMixin OwnerEditMixin
допалняет необходимую инфу (атрибуты) для CreateView и UpdateView
класс для работы с курсом. будет использоваться для функционала Create и Update

ManageCourseListView 
унаследован от - OwnerCourseMixin ListView
Для функционала Read

CourseCreateView 
унаследован от - PermissionRequiredMixin OwnerCourseEditMixin CreateView
Для функционала Create

CourseUpdateView OwnerCourseEditMixin UpdateView
унаследован от - PermissionRequiredMixin OwnerCourseEditMixin UpdateView
Для функционала Update

CourseDeleteView OwnerCourseMixin DeleteView
унаследован от - PermissionRequiredMixin OwnerCourseMixin DeleteView
Для функционала Delete

Атрибуты и методы этих классов:
form_valid(self, form) - определена в ModelFormMixin (from django.views.generic.edit import ModelFormMixin)
или чуть раньше. Не путать с методом is_valid форм.
работает с формами и модельными формами - CreateView, UpdateView. Метод выполняется, когда форма
успешно проходит валидацию.
Поведение по умоланию:
-- сохранение объекта в бд (для модельных форм)
-- перенаправление пользователя на страницу по адресу success_url (для обыных форм)

Пока не до конца понятно как он работает, но он как-то связан с CreateView, UpdateView
про form_valid есть здесь https://docs.djangoproject.com/en/3.2/ref/class-based-views/generic-editing/

Помни, что для CreateView и UpdateView в шаблоне будет доступна переменная из контекта - form

больше всего меня обескуражила строчка form.instance.owner = self.request.user в form_valid(form)
как минимум у обычных форм нету instance как до так и после валидации (во всяком случае у невалидных)

fields (в OwnerCourseEditMixin) поля модели, из которых будет формироваться объект обрабочиками
CreateView и UpdateView. Возможно - по большей части для ModelForm от CreateView и UpdateView

success_url - тоже для CreateView и UpdateView - куда перенаправлять в случае успешной обработки
формы классами CreateView и UpdateView
"""
