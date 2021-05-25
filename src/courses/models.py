from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import (Model, CharField, SlugField,
                              ForeignKey, TextField, DateTimeField,
                              PositiveIntegerField, CASCADE, )


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

    class Meta:
        ordering = ['-created', ]
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.title


class Module(models.Model):
    course = ForeignKey('Course', on_delete=CASCADE, related_name='modules')
    title = CharField(max_length=250)
    description = TextField(blank=True)

    def __str__(self):
        return self.title


class Content(Model):
    module = ForeignKey('Module', on_delete=CASCADE, related_name='contents')
    content_type = ForeignKey(ContentType, on_delete=CASCADE)
    object_id = PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')

# То что мы сделали в модели Content - называется обощенная связь
# Возможность соединить модель Content с любой другой моделью представляющей тип содержимого
# (на самом деле вообще с любой моделью)

# Базовый синтаксис для обощенных связей таков, что нужно создать три поля в модели:
# 1) content_type - ForeignKey на модель ContentType
# 2) object_id - идентификатор связанного объекта (PositiveIntegerField
# 3) item - поле типа GenericForeignKey которое обощает данные из предыдущих двух.

# Только поля content_type и object_id будут иметь столбцы в бд
# поле item (GenericForeignKey) - используется только в python коде, хранится
# в оперативной памяти, позволяет нам получить или задать связанный объект.