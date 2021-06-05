from rest_framework.serializers import ModelSerializer, Serializer, HyperlinkedIdentityField

from courses.models import Subject, Course, Module, Content


# https://www.django-rest-framework.org/api-guide/serializers/

class SubjectModelSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='api:subject_detail_api')

    class Meta:
        model = Subject
        fields = ['id', 'title', 'slug', 'url', ]


class ModuleModelSerializer(ModelSerializer):
    class Meta:
        model = Module
        fields = ['title', 'description', 'order', ]


class CourseModelSerializer(ModelSerializer):
    url_to_enroll = HyperlinkedIdentityField(view_name='api:course_enroll_api')
    url = HyperlinkedIdentityField(view_name='api:courses-detail')
    modules = ModuleModelSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id',
                  'owner',
                  'subject',
                  'title',
                  'slug',
                  'overview',
                  'created',
                  'students',
                  'modules',
                  'url_to_enroll',
                  'url', ]
