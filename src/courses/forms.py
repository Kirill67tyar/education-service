from django import forms
from django.forms import inlineformset_factory

from courses.models import Course, Module

ModuleFormSet = inlineformset_factory(Course,
                                      Module,
                                      fields=['title', 'description', ],
                                      extra=2,
                                      can_delete=True)

# объект одного типа - Module будет связан с объектами другого типа - Course

# fields - поля, которые будут добавлены для каждой формы набора
# (description как? ведь его в модели Сourse - нет)

# extra - количество дополнительных пустных форм модулей
# (помимо тех, что отобразятся)

# can_delete - если установить в True, Django для каждого набора добавит checkbox (чекбокс)
# с помощью которого можно отметить объект к удалению

# я так понимаю, что inlineformset_factory специально для подчиненных моделей, которые связаны с
# главной моделью многие к одному.

# дальше мы работаем с этой формой в обработчике CourseModuleUpdateView courses/views.py
# смотри туда