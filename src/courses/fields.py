from django.db.models import PositiveIntegerField

from django.core.exceptions import ObjectDoesNotExist


class OrderField(PositiveIntegerField):
    """
    for_fields - список или тапл в котором должны содержаться
    названия моделей ForeignKey(ManyToOne для модели где определено поле),
    типа for_fields=['course', ]

    pre_save - метод уже есть в PositiveIntegerField (а может и вообще в Field)
    выполяется перед тем, как Django сохранит поле в бд

    model_instance - экземпляр модели, где определено поле

    self.attname - атрибут экземпляра класса поля,
    дает переменную атрибута в формате str, к которой мы присвоили наше поле

    self.model - модель где определено наше поле

    как создавать классы для полей модели:
    https://docs.djangoproject.com/en/3.2/howto/custom-model-fields/
    """

    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super(OrderField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):

        # если пользователь не задал поле order (OrderField)
        if getattr(model_instance, self.attname) is None:
            try:
                qs = self.model.objects.all()

                # если атрибут for_fields присвоен в при создании экземпляра
                # должен быть присвоен по идее
                if self.for_fields:
                    # создаем параметры для фильтрации
                    query = {field: getattr(model_instance, field) for field in self.for_fields}

                    # т.к. наше в for_fields должны передаваться поля ForeignKey
                    # (Course для Module) то таким образом мы получим все модули
                    # принадлежищие курсу на который будет ссылаться model_instance
                    # по связи Многие к Одному
                    qs = qs.filter(**query)

                # находим из нашего qs последнее поле OrderItem
                last_item = qs.latest(self.attname)

                # присваиваем этому полю 1
                value = last_item.order + 1

            except ObjectDoesNotExist:

                # qs = qs.filter(**query) не найдет другие объекты
                # это означает что наш объект первый
                # и вызовется ошибка ObjectDoesNotExist
                value = 0

            # задаем нашему экземпляру атрибут self.attname со знаением value
            # перед тем как он сохранится
            setattr(model_instance, self.attname, value)
            return value

        # если пользователь задал поле order (OrderField)
        # просто продолжаем поведение метода pre_save
        else:
            return super(OrderField, self).pre_save(model_instance, add)
