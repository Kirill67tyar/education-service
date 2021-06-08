from rest_framework.relations import RelatedField
from rest_framework.serializers import (Serializer,
                                        ModelSerializer,
                                        HyperlinkedIdentityField, )

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
    # url_to_enroll = HyperlinkedIdentityField(view_name='api:course_enroll_api')
    url_to_enroll = HyperlinkedIdentityField(view_name='api:courses-enroll')
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


class ItemRelatedField(RelatedField):
    # to_representation - метод, который определен в базовом Field
    def to_representation(self, value):
        return value.render()


class ContentSerializer(ModelSerializer):
    item = ItemRelatedField(read_only=True)

    class Meta:
        model = Content
        fields = ['order', 'item', ]


class ModuleWithContentsSerializer(ModelSerializer):
    contents = ContentSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ['course',
                  'title',
                  'description',
                  'order',
                  'contents', ]


class ThinCourseSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='api:courses-contents')

    class Meta:
        model = Course
        fields = ['id',
                  'title',
                  'slug',
                  'subject',
                  'url', ]


class CourseWithContentsSerializer(ModelSerializer):
    modules = ModuleWithContentsSerializer(many=True, read_only=True)
    url_to_enroll = HyperlinkedIdentityField(view_name='api:courses-enroll')

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
                  'url_to_enroll', ]
