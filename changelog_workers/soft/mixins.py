from django.db import models
from django.db.models import fields


class ChangeloggableMixin(models.Model):
    """Значения полей сразу после инициализации объекта"""
    _original_values = None

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super(ChangeloggableMixin, self).__init__(*args, **kwargs)
        self._original_values = {}
        for field in self._meta.fields:
            try:
                if type(field) == fields.related.ForeignKey:
                    self._original_values[field.name] = (
                        getattr(self, f'{field.name}_id')
                    )
                else:
                    self._original_values[field.name] = getattr(self, field.name)
            except:
                self._original_values[field.name] = None

    def get_changed_fields(self):
        """
        Получаем измененные данные
        """
        result = {}

        for name, value in self._original_values.items():

            if value != getattr(self, name):

                temp = {}
                temp[name] = getattr(self, name)

                # Дополнительная проверка для полей Foreign Key
                if self._meta.get_field(name).get_internal_type() == ('ForeignKey'):
                    if value != getattr(self, f'{name}_id'):
                        result.update(temp)

                # Для остальных полей просто выдаем результат
                else:
                    result.update(temp)

        return result
