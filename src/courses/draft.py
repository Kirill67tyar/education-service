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


---------------------------------------------------------------------------------------------
                                    apps


from django.apps import apps
apps.get_model(app_label='courses', model_name=model_name)

apps.get_models(), - возвращает список всех кстановленных моделей
apps.get_model(app_label='courses', model_name='model_name') - возвращает конкретно эту модель

https://docs.djangoproject.com/en/3.2/ref/applications/


---------------------------------------------------------------------------------------------
                                Кеширование в django

https://docs.djangoproject.com/en/3.2/topics/cache/

Работа подсистемы кеширования при обработке HTTP-запроса:
1) пытается найти запрошиваемые данных в кеше;
2) если это удалось - возвращает ответ;
3) если данные не нашлись - выполняет такие шаги:
    -- делает запрос в бд и/или вычисления, в соответствии с логикой обработчика,
    -- сохраняет результат в кеш,
    -- возвращает данные в HTTP-ответе.


Доступные бэкэнды кеширования:

1) -- backends.memcached.MemcachedCache, или backends.memcached.PyLibMCCache
import:
from django.core.cache.backends.memcached import MemcachedCache, PyLibMCCache
https://memcached.org/
https://github.com/memcached/memcached/wiki/ReleaseNotes169
https://ru.wikipedia.org/wiki/Memcached
а также гугли Memcached в google
MemcachedCache и PyLibMCCache - бэкэнды для Memcached. Это быстрая и эффективная система кеширования
работающая с оперативной памятью. Какой именно из классов использовать - зависит от того,
как настроить взаимодействие Memcached с python кодом.
Предоставляет хорошую производительность. Используется чаще всего


2) -- backends.db.DatabaseCache
import:
from django.core.cache.backends.db import DatabaseCache
использует в качестве хранилища кешей - базу данных


3) -- backends.filebased.FileBasedCache
import:
from django.core.cache.backends.filebased import FileBasedCache
Сохраняет результаты в файловую систему, сериализует, и хранит каждое кешируемое значение
в отдельном файле.
Настройка в settings.py выглядит так:
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'django_cache'),
    }
}


4) -- backends.locmem.LocMemCache
import:
from django.core.cache.backends.locmem import LocMemCache
Бэкэнд для кеширования в памяти. Используется по умолчанию


5) -- backends.dummy.DummyCache
import:
from django.core.cache.backends.dummy import DummyCache
Фиктивный бэкэнд кеширования, применяемый только при разработке.
Он реализует бэкэнд кеширования, но не сохраняет никакие результаты.



************** Memcached

Это приложение при запуске полуает от операционной системы заданный в настройках
объем оперативной памяти для кеширования. Как только место в памяти заканчивается
memcached перезаписывает старые записи.

Порт для Memcached - 11211
Но можно задать любой другой порт.
Раз есть порт, то скорее представляет из себя какой-то сервер.

Требует установки Memcached,
а также библиотеку python-memcached для взаимодействия с Memcached из python кода

Установка Memcached на Windows 10:
https://stackoverflow.com/questions/59476616/install-memcached-on-windows

Steps to install Memcached on Windows:

1 - Download a stable version, in either 32-bit or 64-bit I have tested the 64-bit version.
2 - Unzip it in some hard drive folder. For example C:\memcached
3 - There will be memcached.exe file in the unzipped folder.
4 - Open a command prompt (need to be opened as administrator).
5 - Run c:\memcached\memcached.exe -d install
For start and stop run following command line

c:\memcached\memcached.exe -d start
c:\memcached\memcached.exe -d stop


python-memcached:
pip install python-memcached
https://pypi.org/project/python-memcached/
https://github.com/linsomniac/python-memcached
https://launchpad.net/python-memcached


Так как Memcached уже установлен, то запуск его следующий:
1 - открываешь коноль как администратор.
2 - заходишь по этому адресу C:\Program Files\memcached>
3 - вводишь memcached.exe -d start (memcached.exe -d install если memcached не установлен)


Для Memcached есть отличный инструмент для анализа ее работы через админку.
django-memcache-status
https://pypi.org/project/django-memcache-status/

Это приложение собирает стату по каждомум рабочему приложению Memcached
и отображает ее на сайте администрирования

Минимальная установка:
1) pip install django-memcache-status
2) добавить в INSTALLED_APPS 'memcache_status',
3) В любой admin.py файл добавить:
admin.site.index_template = 'memcache_status/admin_index.html'


какие поля предоставляет ?

Curr Items	- количество объектов, которые находятся в кеше
Get Hits	- показывает какое кол-во в кеш было произведено успешно
Get Misses	- кол-во неудачных обращений к кешу
Miss Ratio  - выводит результирующую оценку по параметрам Get Hits и Get Misses в процентах.
************** Настройки кеширования в settings.py
https://docs.djangoproject.com/en/3.2/ref/settings/#caches

CACHES - словарь используемый в проекте систем кеширования.
Основная настройка для определения системы кеширования

CACHE_MIDDLEWARE_ALIAS - псевдонимы кешей

CACHE_MIDDLEWARE_KEY_PREFIX - префиксы для ключей кешей.
Когда проект работает с несколькими сайтами, префиксы
позволяют избежать коллизий имен ключей

CACHE_MIDDLEWARE_SECONDS - продолжительность хранения кеширования страниц в секундах


************** CACHES
По сути самая важная настройка для кеширования
Подсистему кеширования проекта конфигурируют с помощью насройки CACHES
Это словарь, который задает параметры конфигурации (ключи python) для каждого бэкэнда.
Параметры для CACHES:

BACKEND - используемый класс для бэкэнда

LOCATION - расположение !результата кеширования. В зависимости от используемой системы кеширования
настройка может принимать значения в виде пути в файловой системе, хоста и порта или имени
для бэкэндов на основе оперативной памяти

KEY_FUNCTION - функция для получения ключа кеша. Она принимает в качестве аргументов префикс,
версию и некоторый начальный ключ в виде строки. Затем преобразует их в ключ, используемый
для кеширования

KEY_PREFIX - префикс для всех ключей бэкэнда

OPTIONS - любые дополнительные параметры, которые может принимать конкретный класс бэкэнда

TIMEOUT - время хранения результата кеширования в секундах. По умолчанию равна 300 с (5 минут)
Если естановить None - срок хранения данных не будет ограничен

VERSION - номер версии кеширования данных. Нужно для добавления версии для кеширования

так CACHES выглядит для FileBasedCache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'django_cache'),
    }
}
а так для MemcachedCache (Memcached)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
Если используется несколько рабочих процессов Memcached,
в настройке LOCATION нужно указать список их адресов.


************** Уровни кеширования

Django поддерживает кеширование представленное на нескольких уровнях:

-- низкоуровневое API - предоставляет возможноть кешировать наименьшую единицу вычислений
(запросы или выисления)

-- уровень обработчиков - кешируются резудбтаты обработки одного HTTP запроса

-- уровень шаблонов - примменяется для добавления в кеш результата генерации HTML шаблона
и его фрагмента

-- уровень сайта - кеширует весь сайт

Кеширование на самом деле не такая простая тема, там есть то изучать.
Нужно хорошо разбираться в механизмах кеширования, чтобы
хорошо обдумать стратегию кеширования.

Да, кеширование предполагает хорошо обдуманную стратегию.

++++++++++++++ Очень важные моменты:

!!! Для начала необходимо оптимизировать наиболее дорогие с точки зрения вычислений
запросы и операции. !!!

!!! Следует избегать установления неограниченного срока хранения данных в кеше,
так можно обезопасить себя от получения неактуальной информации !!!

!!! Работа подсистемы кеширования при обработке HTTP-запроса:
1) пытается найти запрошиваемые данных в кеше;
2) если это удалось - возвращает ответ;
3) если данные не нашлись - выполняет такие шаги:
    -- делает запрос в бд и/или вычисления, в соответствии с логикой обработчика,
    -- сохраняет результат в кеш,
    -- возвращает данные в HTTP-ответе.!!!
+++++++++++++

************** низкоуровневое API кеширования

from django.core.cache import cache

cache.set(key, value, timeout)
cache.get(key)

> cache.set('music_band', 'Король и шут', 20)
> cache.get('music_band')
> 'Король и шут'
> cache.set('music_band', 'Король и шут', 20)
> cache.get('music_band')

Хороший пример низкоуровневого кеширования смотри в обработчике CourseListView (courses.views)


************** кеширование шаблонов

{% load cache %}

{% cache 600 some_name some_value_from_context %}
...some tags and calculates...
{% endcache %}

Не очень понял кеширование шаблонов.
У меня закешировались данные от одного курса к другому из-за этого
cache - название тега
600 - кол-во секунд
some_name - непонятно что, и для его
some_value_from_context - какая-то переменная из контекста, но непонятно для чего.

прочти 370 страницу


************** кеширование результата работы обработчиков (HTTP запросов)

from django.views.decorators.cache import cache_page

для добавления в кеш результатов HTTP запросов в django есть декоратор cache_page
его можно наклеить как и на обработчик (если он функция конечно), так и на шаблон url и установить только время
в качестве ключа будет использоваться url этого http запроса (который может меняться динамиески).

смотри пример использования в students.urls/views.py

вот эт кста удобно.

и в этой библиотеке есть также функция never_cache


************** использование кеширования для сайта

кеширование всего сайта - самый высокоуровневый способ кеширования.

1) нужно добавить два промежуточных слоя:
'django.middleware.cache.UpdateCacheMiddleware', и 'django.middleware.cache.FetchFromCacheMiddleware',
между промежутоным слоем
'django.middleware.common.CommonMiddleware',

MIDDLEWARE = [
    ...
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware', - уже есть в MIDDLEWARE
    'django.middleware.cache.FetchFromCacheMiddleware',
    ...
]

!!! Важно помнить:
промежуточные слои при запросе (HTTP request) выполняются в том порядке,
в котором расположены, а при ответе (HTTP response) - в обратном!
Поэтому порядок расположения имеет значение.

Далее для кеширования всего сайта нужно добавить три константы:

CACHE_MIDDLEWARE_ALIAS = 'default'# - псевдоним кеша
CACHE_MIDDLEWARE_SECONDS = 60 * 5  # 5 minutes
CACHE_MIDDLEWARE_KEY_PREFIX = 'educa'# - префикс для всех ключей чтобы избежать пересечения
# при использовании одного рабочего процесса Memcached с несколькими проектами

Для платформы обучения такой вид кеша не очень подходит, т.к. инфа меняется динамически.
Такой вид кеша подходит для сайтов, где инфа меняется очень редко - в идеале
одностраничных статических сайтов.



---------------------------------------------------------------------------------------------
                                RESTful API

from book:
Иногда в проектах появляется необходимость взаимодейтсвия с другими системами для отображения
данных вашего веб-приложения. Для этих целей реализуется специальный интерфейс,
API (application programming interface), которвый определяет точки взаимодействия двух систем.

Наиболее часто для таких целей используется REST (чтобы организовать API)
REST (Representational State Transfer) - передача состояния управления.
Такой способ взаимодействия основан на ресурсах.
Модель приложения (база данных) - представляет из себя ресурсы,
а HTTP заголовки запросов - действия.

Действия в REST должны быть следующие - Create, Read, Update, Delete

за Create отвечает метод POST
за Read отвечает метод GET
за Update отвечает методы (PUT, PATCH)
за Delete - DELETE

общепринятые форматы взаимодействия RESTful API - JSON и XML

При реализации интерфейса для REST API важно продумать, какие точки доступа будут.

Наиболее часто для построения логики REST APi используется фреймворк Django REST Framework

Если в кратце то RESTful API представляет следующее:

возможность Читать, Создавать, Изменять, Удалять определенные данные из базы данных,
которые мы предоставляем (точка достпа), посредством HTTP методов, через
форматы взаимодействия JSON или XML.

Позволяет другим системам (в основном front-end) взаимодействовать с нашим приложением
(по сути с базой данных напрямую через JSON)


REST API в web это легализованный способ доступа информации, который прописывает обладатель информации
доступ в db
это специальное приложение, которое позволяет распарсить инфу с сайта официально и через формат json
а не с помощью библиотеки BeautifulSoup, где мы вычленяем информацию из тегов.
и кстати даже добавлять, изменять, удалять эту инфу.



Общение клиента с REST API происходит через http методы, и http заголовки

!!!                                                     !!!
REST описывает принципы взаимодействия клиента и сервера,
основанные на понятиях «ресурса» и «глагола» (можно понимать их как подлежащее и сказуемое).
В случае HTTP ресурс определяется своим URI, а глагол — это HTTP-метод.
!!!                                                     !!!
а API - это application programming interface (интерфейс программы для разработика)


Ну и про HTTP:
https://datatracker.ietf.org/doc/html/rfc2616

Очень неплохая статья:
https://habr.com/ru/post/50147/

Отличный пример документации API:
https://ghost.org/docs/content-api/

Потенциальный пример для будущего api
https://developers.themoviedb.org/3/getting-started/introduction

библиотека google translate
https://pypi.org/project/googletrans/
************** Django REST Framework

https://www.django-rest-framework.org/

-- settings --
https://www.django-rest-framework.org/api-guide/settings/

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}
REST_FRAMEWORK - основная константа для настроек django rest framework.
поддерживает множество различных параметров для поведения по умолчанию.

параметр (ключ) DEFAULT_PERMISSION_CLASSES за разрешение по умолчанию для доступа к:
Чтению, Созданию, Изменению, Удалению объектов.

DjangoModelPermissionsOrAnonReadOnly - анонимные пользователи могут только просматривать,
а авторизованные имеют полный CRUD функционал по умолчанию.






************** Serializers (Model, all)

отлиная статья о принципах работы Serilalizer и ModelSerializer и Serilalizer
https://www.django-rest-framework.org/api-guide/serializers/


Сериализаторы, которые мы определяем - могут заимствоваться от 3 классов:
1) Serializer - сериализует обычные python классы (объекты python)
2) ModelSerializer - преобразует объекты моделей Django (превращает в OrderedDict или ReturnList)
3) HyperlinkedModelSerializer - аналогичен классу ModelSerializer, но для связанных объектов
формирует http ссылки а не внешние ключи.
(есть еще поле HyperlinkedIdentityField которое позволяет это сделать в ModelSerializer)


Система проста:

- для функционала Read (list, retrieve), Delete
1) принимает на вход объект модели или Queryset
2) если принимает QuerySet, то нужно указать дополнительный аргумент many=True


- для функционала Create, Update
1) если Create - принимает request.data (по сути словарь, то что приходит с POST/PUT/PATCH запросами)
2) если Update - то принимает сначала экземпляр модели или Queryset в аргумент instance
    а в аргумент data принимает request.data
3) Важный момент, когда у тебя обработчик - класс, унаследованный от GenericAPIView и миксина
в методе perform_create ты не можещь вызывать serializer.data при создании.
ты можешь вызывать validated_data и вызовется OrderedDict при создании новой записи

Далее у serializer (экземпляр класса заимствованного от Serializer или ModelSerializer)
будет доступен аргумент data, где можно посмотреть, что в нем содержится.



************** парсеры и рендеры в django rest framework

https://www.django-rest-framework.org/api-guide/renderers/
https://www.django-rest-framework.org/api-guide/parsers/

DRF работает с форматом взаимодействия JSON.
Нужно как то вычленять из HTTP запроса JSON данные, чтобы можно было с ними работать в python коде
И наоборот, из python кода загружать данные в HTTP запрос, чтобы они были, в формате JSON.
Для этого и нужны рендеры и парсеры

----- парсер позволяет преобразовывать тип данных JSON в dict python:

from io import BytesIO
from rest_framework.parsers import JSONParse

datab = b'{"pk": 1, "title": "programming", "slug": "programming"}'
JSONParser().parse(stream=BytesIO(datab))
{'pk': 1, 'title': 'programming', 'slug': 'programming',}

По сути эта команда делает тоже что и json.loads(), но только не совсем понятна история с байтами

В DRF для получения python объекта из JSON используется класс JSONParses.
Т.е. JSONParses - это парсер DRF. Скорее всего атрибут data в request (request.data)
появляется благодаря парсеру JSONParses


Вот так парсер класс определяется (хотя по умоланию и так стоит JSONParses)
REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ]
}


----- рендер позволяет формировать ответы на запросы к API.
Грубо говоря преобразует объекты python (dict, OrderedDict, ReturnList) в JSON данные

from rest_framework.renderers import JSONRenderer

Для определенния конкретного класса рендерера DRF смотрит на тип объекта, который
нужно преобразовать (dict или QuerySet или экземпляр модели).
тип ответа зависит от заголовка Accept, HTTP запроса

для формирования json ответа будет задействован JSONRenderer

from rest_framework.renderers import JSONRenderer

serializer_data = {'pk': 1, 'title': 'programming', 'slug': 'programming',}
JSONRenderer().render(serializer_data)
b'{"pk":1,"title":"programming","slug":"programming"}'

По умоланию DRF ипользует два рендерера:
JSONRenderer
BrowsableAPIRenderer - предоставляет веб-интерфейс для просмотра API

Воэ эта страница с документацией и формами, которое мы полуаем при обращение к API
приложения с JSON данными из базы данных генерируется благодаря рендереру BrowsableAPIRenderer

Можно указать необходимый класс в настройках:
DEFAULT_RENDERER_CLASSES в константе REST_FRAMEWORK


************** Базовый набор классов и примесей в DRF

https://www.django-rest-framework.org/api-guide/generic-views/

Базовый набор классов и примесей могут использоваться для точек доступа к функциями:
полуения, создания, изменения, удаления объектов.



APIView
from rest_framework.views import APIView

Заимствуется от View.
Отличия от View и особенности:
-- APIView использует собственные классы для объекта запроса и ответа (Request и Response)
-- может обрабатывать исключения APIException (from rest_framework.exceptions import APIException)
возвращая необходимые коды ошибок
-- Реализует методы авторизации и аутентификации, чтобы была возможность ограниить доступ
к обработчику API-запросов

А вообще система довольна проста:

1) Есть базовый APIView.
- Методы get, post, put, patch, delete там придется полностью писать вручную,
вернее начинку этих методов, сам эти методы там есть, т.к. APIView заимствован от View из Django
- Атрибуты queryset, serializer_class, permission_classes, authentication_classes и т.д
там есть

2) Есть:
- GenericAPIView (from rest_framework.generics)
и миксины:
- CreateModelMixin (Create)(from rest_framework import mixins):
- ListModelMixin (Read)
- RetrieveModelMixin (Read)
- UpdateModelMixin (Update)
- DestroyModelMixin (Delete)
Так вот, у этих миксинов есть методы list, retrieve, create, update, partial_update, destroy
(а также perform_create и perform_update)
Эти миксины с этими методами работают только в связке с GenericAPIView

Так что можно создавать классы вручную и наследоваться от миксина и GenericAPIView
А можно использовать из rest_framework.generics типо ListAPIView или RetrieveUpdateDestroyAPIView
Они уже унаследованы от миксинов и GenericAPIView, причем во всех возможных вариантах.

3) Есть ViewSet (from rest_framework.viewsets)
Ситуация схожа с генериками которые уже от всего унаследованы, но добавляется еще класс GenericViewSet
И есть итоговый базовый класс:
- ModelViewSet
С полным CRUD функционалом.
Из преимществ появляется self.action (list, retrieve и т.д.)
И возможность настроить роутер в urls.py

Вот что написано в ModelViewSet  в viewsets.py:

ViewSets are essentially just a type of class based view, that doesn't provide
any method handlers, such as `get()`, `post()`, etc... but instead has actions,
such as `list()`, `retrieve()`, `create()`, etc...

Actions are only bound to methods at the point of instantiating the views.

    user_list = UserViewSet.as_view({'get': 'list'})
    user_detail = UserViewSet.as_view({'get': 'retrieve'})

Typically, rather than instantiate views from viewsets directly, you'll
register the viewset with a router and let the URL conf be determined
automatically.

    router = DefaultRouter()
    router.register(r'users', UserViewSet, 'user')
    urlpatterns = router.urls


************** Обработка аутентификации пользователей в DRF

https://www.django-rest-framework.org/api-guide/authentication/

Прописывается в настройках аутентификация так:
REST_FRAMEWORK = {# REST_FRAMEWORK - базовая константа для настроек DRF
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}
from rest_framework.authentication import BasicAuthentication

В DRF есть классы для управления аутентификацией

-- BasicAuthentication - базовая аутентификация в DRF. Пользователь и пароль отправляются в
зашифрованном виде в заголовке HTTP Authorization
https://en.wikipedia.org/wiki/Basic_access_authentication

-- TokenAuthentication - бэкэнд для авторизации по токену.
Используется модель токен для сохранения токенов, для сохранения токенов пользователей
которые добавляются к запросам в HTTP заголовке Authorization
гугли token authentication и т.д.

-- SessionAuthentication - бэкэнд на основе сессий Django. Полезен, когда браузерный код
отправляет AJAX или другие асинхронные запросы

-- RemoteUserAuthentication - делегирует процесс авторизации пользователя веб-серверу,
который устанавливает переменную окружения REMOTE_USER

Можно создать собственный бэкэнд. Нужно унаследоваться от BasicAuthentication
и описать для него метод authenticate()

!!! Аутентификация только определяет конкретного пользователя, выполняющего запрос. !!!
    Она не ограничивает доступ к обработчикам по ролям.
!!! Для ограничения доступа к обработчикам используются permissions (я так понимаю от DRF)!!!

как добавить аутентификацию в наш обработчик?
Ну если это класс, то через атрибут authentication_classes = (,)

DRF определяет пользователя по HTTP заголовку Authorization
https://developer.mozilla.org/ru/docs/Web/HTTP/Headers/Authorization

заголовок Authorization использует кодировку base64
что не безопасно. Ее можно с лугкостью расшифровать.


В чем недостаток basic authentication в DRF

в headers запроса появляется загловок со значением:
Authorization: Basic a2lyaWxsYm9nb21vbG92LnJpY0B5YW5kZXgucnU6YWxza2RqZmhn

это можно декодировать в utf-8 - https://www.base64decode.org/
Это обычная кодировка base64 и передается в headers каждый раз при GET запросе
Главных недостатка 2:
1 - каждый раз мы светим email и паролем в headers в небезопасной кодировке - очень не безопасно.
2 - лишняя нагрузка на базу данных, ведь каждый раз при таком запросе приходится
сверять email и пароль в базе данных.

Это не как обычная авторизация, когда мы проверяем валидность логина и пароля,
и если всне норм, то запоминаем что это нужный пользователь с помощью сессионого ключа
который создается с помощью функции login().

Здесь мы каждый раз проверяем логин и пароль, что очень не эффективно.

Поэтому лучше использовать систему JWT токен

************** JSON Web Token (JWT)
https://jwt.io/
https://pyjwt.readthedocs.io/en/stable/
https://github.com/Kirill67tyar/pyjwt
https://django-rest-framework-simplejwt.readthedocs.io/en/latest/
https://pypi.org/project/djangorestframework-simplejwt/

Гугли дополнительно про JWT.
Много картинок и схем как это работает.
Вот неплохая статься https://habr.com/ru/post/340146/
она же на английском:
https://morioh.com/p/63009714b79a

И of course wikipedia: https://en.wikipedia.org/wiki/JSON_Web_Token

Картинка JWT:
C:\Users\User\Desktop\Job\learning_tree\tree-of-knowledge\web\JWT\JWT


Там можно выбирать разные алгоритмы формирования этого токена (по умолчанию HS256)

Данный токен представляет из себя короткое время жизни, и предстовляет из себя структуру,
которую можно однозначно идентифицировать

Пример токена:
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.
SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c

Состоит из трех частей:
HEADER:ALGORITHM & TOKEN TYPE
1 часть - голова, где передается алгоритм шифрования и какой это тип токена
{
  "alg": "HS256",
  "typ": "JWT"
}

PAYLOAD:DATA
2 часть - это данные по пользователю (нечувствительные данные имя или id юзера,
или администратор ли он, метаданные в общем) данные чтобы пользователя можно было однозначно идентифицировать
iat - это время жизни этого токена
Как формируются ключи JWT, какие обязательны, какие нет:
https://en.wikipedia.org/wiki/JSON_Web_Token#Standard_fields
{
  "sub": "1234567890",
  "name": "John Doe",
  "iat": 1516239022
}

VERIFY SIGNATURE
3 часть - это пара первых двух частей (headers и payload), которые зашифрованы с помощью секретного
ключа, который знает только сервер
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),

your-256-bit-secret

)

Важно - все эти три данные в токене декодированы base64

* Как это все работает?
1) Когда сервер получает данный токен, он его разбивает на три части по точке
2) При это у сервера есть свой секретный ключ
3) И сервер их шифрует с помощью секретного ключа
4) И если эти данные совпали с тем, что пришло от клиента
точнее совпадает 3 часть токена и то как зашифровал сервер с помощью секретного ключа
значит тому пользователю, что указан во второй части (payload) можно доверять

Дальше как это работает на уровне сервера смотри видео с 8:09 (django API, bot flask)


* Зачем нужно маленькое время жизни данного ключа?
Для того чтобы уменьшить вероятность использования данного токена другими людьми
Если кто-то в HTTP трафике перехватит этот токен, этот токен через 5 мимнут протухнет,
и он уже им воспользоваться не сможет

* Как получить новый токен?
Для этих целей придумана другая структура. Не просто один токен, а пара токенов

"access token" - многоразового использования, но с коротким временем жизни
"refresh token" - одноразовый, но с большим временем жизни

Похоже refresh token это приватный ключ, а access token - публичный ключ
Того токен, что мы разобрази выше это access token который быстро протухает
Его можно много раз использвать, до того, как он протухнет
Как только он протух нужно получить новый access token
Для этого как раз и новый refresh
refresh token позволяет обратиться по определенному адресу, полуить новую пару
access token и refresh token и опять использовать уже новый access token
до времени жизни access token и тд.

Эти токены получаются один раз, когда происходит логирование на сайте.
нормальная авторизация через метод post. Сервер сам выдает эти токены при валидной авторизации

* А как быть, если хакер перехватил и access и refresh token?
Ну походит он по серверу, что-то поделает. Но потом эта пара будет невалидна той,
которую настоящий пользователь получит заново при авторизации.

Система будет видеть что не у пользователя не у хакера не валидный refresh
и таким образом анулируются все токены, нужно будет пройти снова процесс авторизации
и после этого нормальный пользователь получит новые access и refresh, которые будут отличаться
от того, то есть у хакера.

Это в целом безопасная система, которая минимизирует взлом и возможность долго
пользоваться чужим аккаунтом.
Уходит от того, что очень увствительные данные будут использоваться в теле запроса
Будут использоваться только токены. Максимум инфы это возможный id пользователя.


************** djangorestframework-simplejwt
Как работать с библиотекой djangorestframework-simplejwt
для системы токенов
важно - при использовании такой системы authenticated_classes нужно отключать в обработчиках
https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html#installation
https://pypi.org/project/djangorestframework-simplejwt/

* Как установить:
1) pip install djangorestframework-simplejwt
2) добавить 'rest_framework_simplejwt.authentication.JWTAuthentication',
в базовую настройку REST_FRAMEWORK, поднастройку DEFAULT_AUTHENTICATION_CLASSES

REST_FRAMEWORK = {'DEFAULT_AUTHENTICATION_CLASSES': (
        ...
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        )
    ...}
3) в корневом urls.py импортировать TokenObtainPairView и TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
4) добавть в корневой urlpatterns:
path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
5) все, минимальная настройка готова

* Механиз авторизации с token:
1) Для первого раза делаешь post запрос на http://127.0.0.1:8000/api/token/
при этом вставляешь в тело запроса JSON данные
{"email": "kirillbogomolov.ric@yandex.ru",
"password": "alskdjfhg"}
или те, с помощью которых происходит аутентификация на сервере

2) получаешь два токена (в body HTTP-response):
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYyNDMwNTkyNiwianRpIjoiYzlmMjA5Y2NmODRlNDdjOGExZDdjMjZlZjI5Y2FkZjciLCJ1c2VyX2lkIjoxfQ.bVv5YYN8ucakAlTk2pIs-Cx_79_uYzZ-OQLZlaZ1FkE",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI0MjE5ODI2LCJqdGkiOiI1NTZmMmQ1ZmQxZWE0NzQ2ODNiMDRhYmMzZWJmOTY5YSIsInVzZXJfaWQiOjF9.ZCVkefJofX-OqsNZdtEdN9YDYczLml8glQSlxLBb2ls"
}

refresh token - публичный токен который быстро протухает
access token - приватный токен, который нужно сохранить, и менять, когда публичный протухнет
по тому адресу http://127.0.0.1:8000/api/token/refresh/
или можно получть новые refresh и access токены

3) для доступа к контенту
выбираешь способ аутентификации Bearer Token и вставляешь access token в нужное место

4) чтобы обновить access token посылаешь post запрос по адресу (без аутентификации)
http://127.0.0.1:8000/api/token/refresh/
с телом запроса:
{"refresh":
"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.
eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYyNDMwNTkyNiwianRpIjoiYzlmMjA5Y2NmODRlNDdjOGExZDdjMjZlZjI5Y2FkZjciLCJ1c2VyX2lkIjoxfQ.
bVv5YYN8ucakAlTk2pIs-Cx_79_uYzZ-OQLZlaZ1FkE"}
(любой другой refresh token)
и получаешь access token, который можешь дальше использовать

*
refresh token по умолчанию один день
access token по умолчанию 5 минут

в настройках можно менять
https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html
from datetime import timedelta

...

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),# - отвечает за срок годности access token
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),# - отвечает за срок годности refresh token
    ...


Когда ты автризиуешься через Bearer Token то в заголовках HTTP появится такой заголовок:
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI0MjIxNDY5LCJqdGkiOiIzZDNlYjFhZmJmNGY0YjZhOTYyZTM0Y2NkM2EyMTExZSIsInVzZXJfaWQiOjF9.QYDh52m4ixIPo0aqQ0cCjiO_AvMQ1uLP04Wa53FvAwc
(понятно что вместо eyJ0eXAiOiJKV... будет access token)



************** permissions

https://docs.djangoproject.com/en/3.2/topics/auth/default/#permissions-and-authorization
https://www.django-rest-framework.org/api-guide/permissions/

В DRF реализована система доступа пользователей к данным, по анологии с тем, как это
сделано в Django.

Разрешения определенные в DRF:

-- AllowAny - позволено любому

-- IsAuthenticated - доступ имеют только авторизированные пользователи

-- IsAdminUser - только админы имеют доступ

-- IsAuthenticatedOrReadOnly - авторизированные имеют доступ к полному функционалу,
 анонимные только к чтению

-- DjangoModelPermissions - разрешение на основе django.contrib.auth
У обработчиков с таким уровнем должен быть задан QuerySet.
Будут иметь доступ те, кто умеют разрешение на обращение к указанной модели

-- DjangoObjectPermissions - разрешение Django по отношению к конкретным объектам.

Доступ к обработчику в классе прописывается permission_classes = (,)

Если доступ запрещен, то формируется HTTP Ответ с статус кодом:
401 - пользователь не авторизован
403 - доступ запрещен

Да, ну и можно самим определять свои классы доступа (разрешения):

from rest_framework.permissions import BasePermission, SAFE_METHODS
from notes.models import Note

class IsAuthorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True
        return request.user == obj.author


Т.е. надо определить has_permission и has_object_permission

BasePermission - базовый класс, от которого должен наследоваться наш permission

has_permission - выполняет проверку доступа на уровне обработчика
has_object_permission - проверяет доступ к объекту

Чтобы разрешить доступ нужно возвращать True, чтобы запретить - False


---------------------------------------------------------------------------------------------
                    WSGI

https://wsgi.readthedocs.io/en/latest/
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/

Очень, очень хорошая статья
https://habr.com/ru/post/426957/

WSGI (Web Server Gateway Interface) - это интерфейс для взаимодействия
python приложения и веб-сервера. Является своего рода стандартом
при запуске Django-приложений.

Когда мы создаем новый проект с помощью startproject
Django добавляет файл wsgi.py

Он содрежит вызываемый объект, который используется WSGI в качестве точки
входа в приложение. WSGI применим как и для разработки, так и для боевого режима


****** uWSGI

https://uwsgi-docs.readthedocs.io/en/latest/
https://uwsgi-docs.readthedocs.io/en/latest/WSGIquickstart.html
uWSGI (программа) - очень быстрый сервер для python.
Он взаимодействует с python-приложениями посредством WSGI
Именно uWSGI занимается приобразованием запросов в формат,
с которым может рабоать django


Как это все работает для Django:
            :www
            :
            :       HTTP                    Socket                      WSGI
| Client |------------------>| NGINX |------------------>| uWSGI |------------------>| Django |
| browser|<------------------|       |<------------------|       |<------------------|        |
            :

В такой цепочке запрос от клиента обрабатывается в несколько шагов:

1) NGINX принимает HTTP запрос

2) Если запрос на получение статических файлов, его обрабатывает сам NGINX
Если запрос на что-то другое, NGINX делегирует его обрабоку веб-серверу uWSGI через сокет

3) uWSGI принимает входящий запрос, и передает его в Django-приложение.
Результирующий HTTP ответ передается по цепочке в обратном порядке,
и NGINX отправляет его клиенту.

"""

# Прокси сервер - принимает в себя все входяще запросы,
# и распределяет их межд множеством веб-приложений.

from rest_framework.parsers import JSONParser

from django.views.decorators.cache import cache_page

from django.core.cache import cache
# from django.core.cache.backends.memcached import MemcachedCache, PyLibMCCache
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

from django.apps import apps
# apps.get_model(app_label='courses', model_name=model_name)


# 4 способа переопределить работать с User (крутая статья):
# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html

"""
NGINX - 

WSGI - 

uWSGI - 

Как сервер работает для Django:

            :www
            :
__________  :       HTTP     _________        Socket     _________         WSGI      __________ 
| Client |------------------>| NGINX |------------------>| uWSGI |------------------>| Django |
| browser|<------------------|       |<------------------|       |<------------------|        |
----------  :                ---------                   ---------                   ----------
            
В такой цепочке запрос от клиента обрабатывается в несколько шагов:

1) NGINX принимает HTTP запрос

2) Если запрос на получение статических файлов (CSS, JavaScript, Media), его обрабатывает сам NGINX
Если запрос на что-то другое, NGINX делегирует его обрабоку веб-серверу uWSGI через сокет

3) uWSGI принимает входящий запрос, и передает его в Django-приложение.
Результирующий HTTP ответ передается по цепочке в обратном порядке,
и NGINX отправляет его клиенту.
"""