from django.contrib import admin

from courses.models import Module, Course, Subject


# https://docs.djangoproject.com/en/3.2/ref/contrib/admin/

@admin.register(Subject)
class SubjectModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', ]
    prepopulated_fields = {'slug': ('title',)}


class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Course)
class CourseModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'created', ]
    list_filter = ['created', 'subject', ]
    search_fields = ['title', 'overview', ]
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline, ]
