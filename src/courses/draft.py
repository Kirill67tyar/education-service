"""
Content Management System (CMS) - система управления содержимым

---------------------------------------------------------------------------------------------
                        Фикстуры

https://software-testing.ru/library/testing/testing-automation/3357-pytest-the-awesome-parts-fixtures
https://qna.habr.com/q/70560

Фикстуры - это по сути тестовые данные. Они нужны для unit-тестирования.
Это могут быть как данные в базе, так и обычные файлы (обычно 2 варианта, до и после обработки так скажем).
Каждый раз когда запускаются тесты, эти данные используются для установления начального состояния системы,
что бы тесты всегда выполнялись предсказуемо.

Для функционального тестирования (тестрирование контроллеров, интаграционных тестов) фикстуры не применяются,
хотя суть там так же сходна. Если честно, то тут мнение расходится. Одни говорят что при функциональных тестах
нельзя использовать даже моки, то есть система в процессе выполнения тестов полностью создает то состояние
которое необходимо для других тестов. Например последовательное выполнение тестов на добавление статьи и
ее просмотр. Другие же предпочитают для каждого тесткейса выставлять состояние с нуля.
По сути это схоже с использованием фикстур, но реализация различается.
У вас есть некое api для заполнения данными (скажем метод добавляющий пользователя),
и перед выполнением тест-кейса происходит ресет данных и заполнение их новыми.
Плюсы так же есть - можно распаралелить выполнение тестов. (но не верьте мне на слово)

Миграции - механизм организации версионности структуры проекта.
Вы можете написать миграцию для изменения местоположения статики
(картинки, поменять ссылки в базе и т.д.), или же у вас добавляется новая таблица/поле.
Обычно дополняется обратной миграцией, которая восстанавливает исходную структуру.
Обязательно для работы в команде или при частом изменении организации данных в проекте,
вообще я бы посоветовал использовать их всегда.

Django поддурживает форматы JSON, XML и даже YAML

Основные две команды, как загружать и выгружать данные из db

python manage.py dumpdata   - выгружает дынные из db
python manage.py loaddata   - загружает дынные в db

Пример использования:
python manage.py dumpdata courses --indent=2

Такая команда выгрузит данные из всех моделей, из приложения courses
в формате JSON (по умолчанию) с пробелом 2(--indent=2)
можно применить флаг --format чтобы задать формат вывода

как сохранить в какой-то файл?
python manage.py dumpdata courses --indent=2 --output=courses/fixtures/subjects.json

Как получить инфу о всех параметрах dumpdata?
python manage.py dumpdata --help

Команда для того, чтобы загрузить данные в db:
python manage.py loaddata subjects.json

Но, но, но...
Есть одна проблемка. Если данные на русском языке, то они выгрузятся с кодировкой UTF-8
и обратно не загрузятся. Такие дела.
Гуглил как решить эту issue, но так и не нашел, такое ощущение, что эта проблема только у меня.

По умолчанию django ищет фикстуры в папке fixtures/ каждого приложения, но можно указать полный
путь до них. Также есть возможность задать каталоги где искать фикстуры
с помощью константы FIXTURE_DIRS в settings.py

Фикстуры - отличный способ заполнить базу данных начальными объектами, также
очень удобно применять их при тестировании.

Про фикстуры и тестирование в doc:
https://docs.djangoproject.com/en/3.2/topics/testing/
https://docs.djangoproject.com/en/3.2/ref/django-admin/#django-admin-loaddata
https://docs.djangoproject.com/en/3.2/howto/initial-data/


Но если данные на английском языке, то все нормально выгружает и загружает:
$ python manage.py dumpdata courses --indent=2 --format=json --output=courses/fixtures/subjects.json

$ python manage.py loaddata subjects.json
Installed 5 object(s) from 1 fixture(s)


---------------------------------------------------------------------------------------------
                        Виды наследования моделей Django

3 вида наследования моделей:

1) абстрактные модели
2) наследование с помощью нескольких таблиц
3) прокси модели

------- Абстрактная модель
from django.contrib.auth.models import AbstractUser
Абстрактная модель - это базовый класс. В нем необходимо определить поля, которые будут общими для
всех дочерних классов.
Абстрактные модели полезны, когда нужно описать некую общую базовую информацию.
(вспомни AbstractUser, AbstractBaseUser). Для абстрактоной модели не создается таблица в бд
а вот в модели, от которой она наследуется создается.

Как сделать абстрактную модель? присвоить атрибут abstract = True в классе Meta модели.

Пример абстрактной модели BaseContent и дочерней Text

class BaseContent(Model):
    title = CharField(max_length=250)
    created = DatetimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Text(BaseContent):
    body = TextField()

В этом случае в бд будет создана только одна таблица - Text (<app_name>_text).


------- Наследование с несколькими таблицами
В случае наследования с несколькими таблицами, для каждой модели создается соответствующая таблица.
Для каждой из моделей создается своя собственная таблица
Django делает ссылку OneToOneField на родительскую модель из дочерней.
Чтобы применить этот метод нужно просто унаследовать дочерней модели от родительской.

class BaseContent(Model):
    title = CharField(max_length=250)
    created = DatetimeField(auto_now_add=True)

class Text(BaseContent):
    body = TextField()

Не совсем понятно для чего она, какие у нее преимущества и недостатки.

------- Прокси-модели
Они используются когда модели хранят одинаковые данные но поведение классов отличается.
Полезно, когда мы хотим реализовать для каждой из моделей отдельную функциональность
(методы, переопределить или добавить менеджеры, использовать другие опции класса Meta)
Разумеется таблицы для proxy-моделей в бд не создаются.

как определить proxy модель? добавить атрибут proxy=True в класс Meta модели.

Пример proxy модели:

class BaseContent(Model):
    title = CharField(max_length=250)
    created = DatetimeField(auto_now_add=True)


class OrderingContent(BaseContent):

    class Meta:
        proxy = True
        ordering = [-'created',]

    def created_delta(self):
        return timezone.now() - self.created

В донном случае OrderingContent добавит сортировку по умолчанию для QuerySet и метод created_delta

Очень полезная статья, но немного не по теме
https://docs.djangoproject.com/en/3.2/ref/models/fields/


---------------------------------------------------------------------------------------------
                        Примеси (Mixins)

https://docs.djangoproject.com/en/3.2/topics/class-based-views/mixins/

Примиси (Mixins) - это класс, который используется при множественном наследовании.
При определении класса можно задействовать несколько примесей, каждая из которых добавит
часть функций в класс.
Примеси удобны в двух случаях:
1 - нужно использовать несколько различных функций в рамках моего класса
2 - реализовать одну и туже функциональность в нескольких классах

В rest_framework тоже используются миксины для CRUD функционала
Вспомни, миксины в rest_framework добавляют нам функционал list, retrieve,create, update, partial_update, destroy
И работают они совместно с GenericAPIView

Чтобы определять самому миксины - нужно хорошо разбираться в django, какие методы, за что отвечают,
какие вызываются и когда, какие атрибуты используются.

*****Разбор классов обработчиков, и логики кастомных миксинов*****

OwnerMixin
базовый миксин для работы owner.

OwnerEditMixin - для CreateView и UpdateView (переопределяем form_valid), для работы с owner

OwnerCourseMixin
унаследован от - OwnerMixin
класс для работы с курсом. будет использоваться для функционала Read и Delete

OwnerCourseEditMixin
унаследован от - OwnerCourseMixin OwnerEditMixin
допалняет необходимую инфу (атрибуты) для CreateView и UpdateView
класс для работы с курсом. будет использоваться для функционала Create и Update

ManageCourseListView OwnerCourseMixin ListView
Для функционала Read

CourseCreateView OwnerCourseEditMixin CreateView
Для функционала Create

CourseUpdateView OwnerCourseEditMixin UpdateView
Для функционала Update

CourseDeleteView OwnerCourseMixin DeleteView
Для функционала Delete

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
CreateView и UpdateView. Возможно - по большей части для form от CreateView и UpdateView

success_url - тоже для CreateView и UpdateView - куда перенаправлять в случае успешной обработки
формы классами CreateView и UpdateView


Т.е. грубо говоря примеси(миксины) - нужны для определенной функциональности.

Благодаря миксинам мы создаем возможность делать то-то. И дальше в разных классах можем
это использовать

---------------------------------------------------------------------------------------------
                                Permissions

https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#custom-permissions

У user django есть атрибут is_superuser. Если он True - то django даст доступ такому пользователю
ко всем возможностям системы.

В django определено две примиси для ограничения доступа:
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

LoginRequiredMixin
PermissionRequiredMixin

для PermissionRequiredMixin нужно добавлять атрибут permission_required =
примесь PermissionRequiredMixin добавляет проверку налиия у пользователя разрешения
указанного в атрибуте permission_required.
Так обработчики будут доступны только пользователям, имеющим соответствующее разрешение

обрати внимание, что в бд у нас есть две таблицы:
auth_permissions и auth_group_permissions

а в auth_permissions есть столбик code_name

от туда мы можем брать permissions (permission_required)



---------------------------------------------------------------------------------------------
                                    formsets

https://docs.djangoproject.com/en/3.2/topics/forms/formsets/
https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/#model-formsets

В Django предусмотрен механизм работы с несколькими формами на одной странице
Такая группа состоящая из нескольких форм называется набором форм, или формсетами.

is_valid() - позволяет проверить валидность всех входящих в него форм за один раз.

За что отвечает formset (model-formsets)?
-- позволяет отображать несколько объектов типо Form и ModelForm (отправляется эти объекты на сервер за один раз)
-- определяет кол-во форм
-- определяет какое кол-во полей нужно отображать при редактировании объектов
-- устанавливает ограничение на максимальное кол-во создаваемых объектов


***** from courses.forms*****
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

"""

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
from django.contrib.auth.models import AbstractUser

