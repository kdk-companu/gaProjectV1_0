from django.utils import timezone

from django.db import models
from django.urls import reverse
from transliterate import translit
from django.template.defaultfilters import slugify
from workers.models import Subdivision, Department
from workers.models import User


class Organization(models.Model):
    '''Фирма'''
    STATUS_CHOICES = (
        ('customer', 'Заказчик'),
        ('exploitation', 'Эксплуатация'),
        ('designer', 'Проектировщик'),
    )
    name = models.CharField(max_length=255, unique=True, verbose_name='Фирма')
    status = models.CharField(verbose_name='Направление фирмы', choices=STATUS_CHOICES, max_length=50,
                              default='customer')
    site = models.URLField(max_length=255, unique=False, blank=True, verbose_name='Сайт')
    description = models.TextField(verbose_name='Описание фирмы', blank=True)
    slug = models.SlugField(max_length=100, unique=True, db_index=True,
                            verbose_name='URL')  # unique - Уникальное,db_index - индексируемое

    def __str__(self):
        return self.name

    # Админка на русском языке
    class Meta:
        verbose_name = 'Фирма'
        verbose_name_plural = 'Фирмы'  # Во множественнмо числе
        ordering = ['pk']  # Сортировка по каким полям, - обратная сортировка

    def save(self, **kwargs):
        self.slug = slugify(translit(self.name, 'ru', reversed=True))
        super(Organization, self).save()

    # для создание ссылок. И использование ее в html
    def get_absolute_url(self):
        return reverse('organization_view', kwargs={'organization_slug': self.slug})


class Status_Projects(models.Model):
    CURRENT_STATE_CHOICES = (
        ('Done', 'Отсутсвует'),
        ('Project development', 'Разработка проекта'),
        ('Factory tested', 'Заводская испытания'),
        ('Waiting adjustment', 'Ожидание наладки'),
        ('Commissioning works', 'Пусконаладочные работы'),
        ('Waiting trial operation', 'Ожидание опытной эксплуатация'),
        ('Trial operation', 'Опытная эксплуатация'),
        ('Completed projects', 'Законченный проект'),
    )
    STAGE_STATUS_CHOICES = (
        ('Done', 'Выполнено'),
        ('Not_done', 'Не выполнено'),
        ('Running', 'Выполняется'),
        ('Suspended', 'Приостановлено'),
    )

    сurrent_state = models.CharField(verbose_name='Статус проекта', choices=CURRENT_STATE_CHOICES,
                                     max_length=50, default='Not_done')
    #####
    status_factory_tested = models.CharField(verbose_name='Заводская испытания', choices=STAGE_STATUS_CHOICES,
                                             max_length=50, default='Not_done')
    ####
    status_commissioning_works = models.CharField(verbose_name='Пусконаладочные работы', choices=STAGE_STATUS_CHOICES,
                                                  max_length=50, default='Not_done')
    ####
    status_trial_operation = models.CharField(verbose_name='Пусконаладка', choices=STAGE_STATUS_CHOICES, max_length=50,
                                              default='Not_done')
    ####
    status_trial_operation = models.CharField(verbose_name='Опытная эксплуатация', choices=STAGE_STATUS_CHOICES,
                                              max_length=50, default='Not_done')
    ####
    status_completed_projects = models.CharField(verbose_name='Законченный проект', choices=STAGE_STATUS_CHOICES,
                                                 max_length=50, default='Not_done')
    ####
    status_completed_projects = models.CharField(verbose_name='Законченные проекты', choices=STAGE_STATUS_CHOICES,
                                                 max_length=50, default='Not_done')
