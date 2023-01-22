from django.contrib.auth.models import Group
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.urls import reverse
from transliterate import translit
from django.template.defaultfilters import slugify

from changelog_workers.soft.mixins import ChangeloggableMixin
from changelog_workers.soft.signals import journal_save_handler, journal_delete_handler


class Subdivision(ChangeloggableMixin, models.Model):
    '''Описания управлений'''
    name = models.CharField(max_length=150, unique=True, verbose_name='Управление/Подразделение')
    abbreviation = models.CharField(max_length=100, unique=True, verbose_name='Сокращенное название')
    description = models.CharField(max_length=255, blank=True, verbose_name='Описание')  # blank=True Пустое имя поля
    slug = models.SlugField(max_length=100, unique=True, db_index=True,
                            verbose_name='URL')  # unique - Уникальное,db_index - индексируемое

    def __str__(self):
        return self.name + " (" + self.abbreviation + ")"

    # для создание ссылок. И использование ее в html
    def get_absolute_url(self):
        return reverse('subdivision_update', kwargs={'subdivision_slug': self.slug})


    # Админка на русском языке
    class Meta:
        verbose_name = 'Структура. Управление'
        verbose_name_plural = 'Структура. Управления'  # Во множественнмо числе
        ordering = ['pk']  # Сортировка по каким полям, - обратная сортировка

    def save(self, **kwargs):
        self.slug = slugify(translit(self.abbreviation, 'ru', reversed=True))
        super(Subdivision, self).save()


class Department(ChangeloggableMixin, models.Model):
    '''Описание отдела'''
    name = models.CharField(max_length=150, unique=True, verbose_name='Отдел')
    abbreviation = models.CharField(max_length=100, unique=True, verbose_name='Сокращенное название')
    description = models.CharField(max_length=255, blank=True, verbose_name='Описание')  # blank=True Пустое имя поля
    slug = models.SlugField(max_length=100, unique=True, db_index=True,
                            verbose_name='URL')  # unique - Уникальное,db_index - индексируемое

    def __str__(self):
        return self.name + " (" + self.abbreviation + ")"

    def get_absolute_url(self):
        return reverse('department_update', kwargs={'department_slug': self.slug})

    class Meta:
        verbose_name = 'Структура. Отдел'
        verbose_name_plural = 'Структура. Отделы'  # Во множественнмо числе
        ordering = ['pk']  # Сортировка по каким полям, - обратная сортировка

    def save(self, **kwargs):
        self.slug = slugify(translit(self.abbreviation, 'ru', reversed=True))
        super(Department, self).save()


class Chief(ChangeloggableMixin, models.Model):
    '''Описание должностей.'''
    name = models.CharField(max_length=150, unique=True, verbose_name='Должность')
    abbreviation = models.CharField(max_length=100, unique=True, verbose_name='Сокращенное название')
    rights = models.IntegerField(default=0, unique=True, verbose_name='Уровень доступа')
    slug = models.SlugField(max_length=100, unique=True, db_index=True,
                            verbose_name='URL')  # unique - Уникальное,db_index - индексируемое
    group = models.ForeignKey(Group, on_delete=models.PROTECT, blank=True,
                              null=True, verbose_name='Группы')

    def __str__(self):
        return self.name + " (" + self.abbreviation + ")"

    def get_absolute_url(self):
        return reverse('chief_update', kwargs={'chief_slug': self.slug})

    class Meta:
        verbose_name = 'Структура. Должность'
        verbose_name_plural = 'Структура. Должности'  # Во множественнмо числе
        ordering = ['rights']  # Сортировка по каким полям, - обратная сортировка

    def save(self, **kwargs):
        self.slug = slugify(translit(self.abbreviation, 'ru', reversed=True))
        super(Chief, self).save()


@receiver(post_save, sender=Chief)
def post_save_receiver(sender, instance, created, raw, using, **kwargs):
    if created:
        group_save = Group.objects.create(name=instance.name)
        Chief.objects.filter(id=instance.pk).update(group=group_save)
    else:
        Group.objects.filter(id=instance.group.pk).update(name=instance.name)


@receiver(post_delete)
def post_delete_receiver(sender, instance, using, **kwargs):
    try:
        remove = Group.objects.filter(id=instance.group.pk)
        remove.delete()
    except Exception:
        pass


# Логирование
post_save.connect(journal_save_handler, sender=Subdivision)
post_delete.connect(journal_delete_handler, sender=Subdivision)

post_save.connect(journal_save_handler, sender=Department)
post_delete.connect(journal_delete_handler, sender=Department)

post_save.connect(journal_save_handler, sender=Chief)
post_delete.connect(journal_delete_handler, sender=Chief)
