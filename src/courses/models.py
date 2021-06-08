# from django.db import models
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import (Model, CharField, SlugField,
                              ForeignKey, TextField, DateTimeField,
                              PositiveIntegerField, FileField, URLField,
                              ManyToManyField, CASCADE, )

from courses.fields import OrderField


class Subject(Model):
    title = CharField(max_length=250)
    slug = SlugField(max_length=250, unique=True)

    class Meta:
        ordering = ['title', ]
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    def __str__(self):
        return self.title


class Course(Model):
    owner = ForeignKey(User, on_delete=CASCADE, related_name='courses_created')
    subject = ForeignKey('Subject', on_delete=CASCADE, related_name='courses')
    title = CharField(max_length=250)
    slug = SlugField(max_length=250, unique=True)
    overview = TextField()
    created = DateTimeField(auto_now_add=True)
    students = ManyToManyField(User, related_name='courses_joined', blank=True)

    class Meta:
        ordering = ['-created', ]
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.title


class Module(Model):
    course = ForeignKey('Course', on_delete=CASCADE, related_name='modules')
    title = CharField(max_length=250)
    description = TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course', ])

    def __str__(self):
        return f'{self.order}. {self.title}'

    class Meta:
        ordering = ['order', ]


class Content(Model):
    module = ForeignKey('Module', on_delete=CASCADE, related_name='contents')
    content_type = ForeignKey(ContentType,
                              limit_choices_to={'model__in': ('text',
                                                              'video',
                                                              'image',
                                                              'file',)}, on_delete=CASCADE)
    object_id = PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module', ])

    class Meta:
        ordering = ['order', ]


# То что мы сделали в модели Content - называется обобщенная связь
# Возможность соединить модель Content с любой другой моделью представляющей тип содержимого
# (на самом деле вообще с любой моделью)

# Базовый синтаксис для обобщенных связей таков, что нужно создать три поля в модели:
# 1) content_type - ForeignKey на модель ContentType
# 2) object_id - идентификатор связанного объекта (PositiveIntegerField
# 3) item - поле типа GenericForeignKey которое обобщает данные из предыдущих двух.

# Только поля content_type и object_id будут иметь столбцы в бд
# поле item (GenericForeignKey) - используется только в python коде, хранится
# в оперативной памяти, позволяет нам получить или задать связанный объект.

# Модель Content определяет обощенную связь с различными типами содержимого

# Очень важный момент - если ты хочешь сериализовать таблицу ссылающуюся
# на ContentType с помощью обощенной связи, то смотри на классы в courses/api/serializers.py:
# - ItemRelatedField
# - ContentSerializer

# Там все понятно, только должен быть определен метод render (или какой другой метод)

# Про limit_choices_to есть здесь:
# https://docs.djangoproject.com/en/3.2/ref/models/fields/
"""
limit_choices_to

Sets a limit to the available choices for this field when this field is rendered using a 
ModelForm or the admin (by default, all objects in the queryset are available to choose). 
Either a dictionary, a Q object, or a callable returning a dictionary or Q object can be used.

For example:

staff_member = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    limit_choices_to={'is_staff': True},
)
causes the corresponding field on the ModelForm to list only Users that have is_staff=True. 
This may be helpful in the Django admin.
"""


# Мое мнение - это такой дополнительный параметр для фильтрации.
# Таким образом мы ограничиваем типы содержимого ContentType
# Чтобы фильтровать объекты ContentType при запросах - указали условие model__in=('text', ...)


class AbstractBaseItem(Model):
    owner = ForeignKey(User, on_delete=CASCADE, related_name='%(class)s_related')
    title = CharField(max_length=250)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def render(self):
        model_name = self._meta.model_name.lower()
        template_name = f'courses/content/{model_name}.html'
        return render_to_string(template_name=template_name, context={'item': self, })


# благодаря related_name='%(class)s_related'
# у модели User создадутся менеджеры объектов:
# file_related,
# image_related,
# text_related,
# video_related

class Text(AbstractBaseItem):
    content = TextField()


class File(AbstractBaseItem):
    file = FileField(upload_to='files')


class Image(AbstractBaseItem):
    file = FileField(upload_to='images')


class Video(AbstractBaseItem):
    url = URLField()
