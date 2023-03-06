import datetime

from django.urls import reverse
from django.utils import timezone

from django.db import models

from transliterate import translit
from django.template.defaultfilters import slugify

from projects.models import Organization
from workers.models import Subdivision, Department, User


class Organizations_Objects(models.Model):
    """Название объекта"""
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name='Эксплуатирующая организация')
    name = models.CharField(max_length=255, unique=True, verbose_name='Название объекта')
    name_tables = models.CharField(max_length=80, unique=True, blank=False, verbose_name='Название для табеля')
    short_names = models.CharField(max_length=80, unique=True, blank=True, verbose_name='Обиходные название')
    description = models.TextField(verbose_name='Описание объекта', blank=True)
    property_location = models.TextField(verbose_name='Расположение объекта. Транспорт.', blank=True)
    pay_weekend = models.BooleanField(default=False, verbose_name='Оплата выходных')
    pay_processing = models.BooleanField(default=False, verbose_name='Оплата переработки')
    development_tasks = models.ManyToManyField('Development_Task', blank=True, related_name='development_tasks',
                                              verbose_name='Задание на разработку')
    position_objects = models.ManyToManyField('Position_Object', blank=True, related_name='position_objects',
                                              verbose_name='Позиция на объекте')

    slug = models.SlugField(max_length=150, unique=True, db_index=True,
                            verbose_name='URL')

    def __str__(self):
        return self.organization.name + ". " + self.name

    def save(self, **kwargs):
        self.slug = slugify(translit(str(self.name), 'ru', reversed=True))
        super(Organizations_Objects, self).save()

    def get_absolute_url(self):
        return reverse('organizations_objects_edit', kwargs={'organizations_objects_slug': self.slug})

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'
        ordering = ['pk']


class Project(models.Model):
    """Проект на разработку"""
    POSITION_STATUS_CHOICES = (
        ('New_Object', 'Новый объект'),
        ('Overhaul', 'Капитальный ремонт'),
        ('Reconstruction', 'Реконструкция'),
        ('Modernization', 'Модернизация'),
    )

    organizations_objects = models.ForeignKey(Organizations_Objects, on_delete=models.PROTECT, blank=False, null=True,
                                              verbose_name='Название объекта')
    name = models.CharField(max_length=250, unique=False, verbose_name='Название проекта')
    contract_number = models.CharField(max_length=150, unique=True, blank=True, verbose_name='Номер договора/контракта')
    construction = models.CharField(max_length=250, blank=True, verbose_name='Стройка')
    customer = models.ForeignKey(Organization, on_delete=models.PROTECT, blank=False, null=True,
                                 related_name='organization1', verbose_name='Заказчик')
    exploitation = models.ForeignKey(Organization, on_delete=models.PROTECT, blank=False, null=True,
                                     related_name='organization2', verbose_name='Эксплуатация')
    date_issue = models.DateTimeField(default=timezone.now, verbose_name='Дата регистрации задания')
    status_systems = models.CharField(verbose_name='Статус системы', choices=POSITION_STATUS_CHOICES, max_length=50,
                                      default='New_Object')
    slug = models.SlugField(max_length=150, unique=True, db_index=True, verbose_name='URL')

    def save(self, **kwargs):
        self.slug = slugify(translit(str(self.name), 'ru', reversed=True))
        super(Project, self).save()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('projects_edit', kwargs={'project_slug': self.slug})

    class Meta:
        verbose_name = 'Проект на разработку'
        verbose_name_plural = 'Проекты на разработку'
        ordering = ['date_issue']


class Development_Task(models.Model):
    """Задание на разработку"""
    STATUS_COMPLETION_CHOICES = (
        ('Done', 'Выполнено'),
        ('Not_done', 'Не выполнено'),
        ('Running', 'Выполняется'),
        ('Suspended', 'Приостановлено'),
    )
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
    tasks_ppo = models.CharField(max_length=60, unique=True, verbose_name='Задания на ППО')
    name = models.CharField(max_length=250, unique=False, verbose_name='Название системы')
    organizations_objects = models.ForeignKey(Organizations_Objects, on_delete=models.PROTECT, blank=False, null=True,
                                              related_name='organizations_objects', verbose_name='Название объекта')
    project = models.ForeignKey(Project, on_delete=models.PROTECT, blank=False, null=True, related_name='project',
                                verbose_name='Название проекта')
    gip = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='ГИП')
    designer = models.ForeignKey(Organization, on_delete=models.PROTECT, blank=False, null=True,
                                 related_name='designer', verbose_name='Проектировщик')
    part_equipment = models.TextField(blank=True, verbose_name='Состав оборудования')
    task = models.TextField(verbose_name='Описание задания')
    documentation_development = models.TextField(blank=True, verbose_name='Разрабатываемая документация')
    date_documentation_development_planned = models.DateField(verbose_name='Разработка документации. Планируемая.',
                                                              null=True, blank=True)
    date_documentation_development_actual = models.DateField(verbose_name='Разработка документации. Фактическая.',
                                                             null=True, blank=True)
    date_software_development_planned = models.DateField(verbose_name='Разработка ППО. Планируемая.', null=True,
                                                         blank=True)
    date_software_development_actual = models.DateField(verbose_name='Разработка ППО. Фактическая.', null=True,
                                                        blank=True)
    date_equipment_assembly_planned = models.DateField(verbose_name='Сборка оборудования. Планируемая.',
                                                       null=True, blank=True)
    date_equipment_assembly_actual = models.DateField(verbose_name='Сборка оборудования. Фактическая.', null=True,
                                                      blank=True)
    date_factory_acceptance_planned = models.DateField(verbose_name='Заводская приемка. Планируемая.',
                                                       null=True, blank=True)
    date_factory_acceptance_actual = models.DateField(verbose_name='Заводская приемка. Фактическая.',
                                                      null=True, blank=True)
    date_shipment_equipment_planned = models.DateField(verbose_name='Отгрузка оборудования. Планируемая.',
                                                       null=True, blank=True)
    date_shipment_equipment_actual = models.DateField(verbose_name='Отгрузка оборудования. Фактическая.',
                                                      null=True, blank=True)
    source_data_folder = models.TextField(verbose_name='Исходные данные')
    project_archives_folder = models.TextField(blank=True, verbose_name='Папка с проектом')

    status = models.CharField(verbose_name='Отметка выполнения', choices=STATUS_COMPLETION_CHOICES, max_length=50,
                              default='Not_done')
    current_state = models.CharField(verbose_name='Статус проекта', choices=CURRENT_STATE_CHOICES, max_length=50,
                                     default='Done')
    subdivision = models.ForeignKey(Subdivision, on_delete=models.CASCADE, verbose_name='Задание на управлении')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='Задание на отделе')
    date_issue = models.DateTimeField(default=timezone.now, verbose_name='Дата регистрации задания')
    slug = models.SlugField(max_length=250, unique=True, db_index=True, verbose_name='URL')

    def save(self, **kwargs):
        self.slug = slugify(translit("{0} - {1}".format(self.tasks_ppo, self.name), 'ru', reversed=True))
        super(Development_Task, self).save()

    def __str__(self):
        return "{0}. {1}".format(self.tasks_ppo, self.name)

    def get_absolute_url(self):
        return reverse('development_task_detailed', kwargs={'development_task_slug': self.slug})

    class Meta:
        verbose_name = 'Задание на разработку'
        verbose_name_plural = 'Задания на разработку'
        ordering = ['date_issue']


def folder_reviewer_protocol(instance, filename):
    file_name = "Протокол проверки. " + instance.organizations_objects.name + "." + str(
        datetime.datetime.now()) + ".pdf"
    return 'projects/{0}/{1}/{2}'.format(instance.organizations_objects.organization.pk,
                                         instance.organizations_objects.pk, file_name)


class Position_Object(models.Model):
    """Позиция на объекте"""
    STATUS_COMPLETION_CHOICES = (
        ('Done', 'Выполнено'),
        ('Not_done', 'Не выполнено'),
        ('Running', 'Выполняется'),
        ('Suspended', 'Приостановлено'),
    )
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
    organizations_objects = models.ForeignKey(Organizations_Objects, on_delete=models.PROTECT, blank=False, null=True,
                                              verbose_name='Название объекта')
    development_task = models.ForeignKey(Development_Task, on_delete=models.PROTECT, blank=False, null=True,
                                         verbose_name='Задания на ППО')
    name = models.CharField(max_length=255, unique=True, verbose_name='Название позиции')
    short_names = models.CharField(max_length=80, unique=False, blank=True, verbose_name='Обиходные название')
    description = models.TextField(verbose_name='Описание позиции', blank=True)
    status = models.CharField(verbose_name='Отметка выполнения', choices=STATUS_COMPLETION_CHOICES, max_length=50,
                              default='Not_done')
    сurrent_state = models.CharField(verbose_name='Статус проекта', choices=CURRENT_STATE_CHOICES, max_length=50,
                                     default='Done')
    checker = models.ManyToManyField(User, related_name='checker_user', blank=True, verbose_name='Проверяющие')
    reviewer_protocol = models.FileField(upload_to=folder_reviewer_protocol, verbose_name='Протокол проверки шкафов',
                                         null=True, blank=True)
    date_issue = models.DateTimeField(default=timezone.now, verbose_name='Дата добавления позиции.')
    slug = models.SlugField(max_length=250, unique=True, db_index=True, verbose_name='URL')

    def save(self, **kwargs):
        self.slug = slugify(translit(self.name, 'ru', reversed=True))
        super(Position_Object, self).save()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('position_objects_detailed', kwargs={'position_objects_slug': self.slug})

    class Meta:
        verbose_name = 'Позиция на объекте'
        verbose_name_plural = 'Позиции на объектах'
        ordering = ['date_issue']


class Сabinet(models.Model):
    """Шкаф"""
    position_objects = models.ForeignKey(Position_Object, on_delete=models.PROTECT, blank=False, null=True,
                                         verbose_name='Позиция на объекте')
    name = models.CharField(max_length=255, unique=True, verbose_name='Название шкафа')
    factory_number = models.CharField(max_length=255, unique=True, verbose_name='Заводской номер')
    description = models.TextField(verbose_name='Описание', blank=True)
    constructor = models.ManyToManyField(User, related_name='constructor_user', blank=True, verbose_name='Конструктор')
    cabinet_assembler = models.ManyToManyField(User, related_name='cabinet_assembler_user', verbose_name='Сборщик')
    comments = models.TextField(verbose_name='Замечание по шкафу', blank=True)
    date_issue = models.DateTimeField(default=timezone.now, verbose_name='Дата добавления')
    slug = models.SlugField(max_length=150, unique=True, db_index=True, verbose_name='URL')

    def save(self, **kwargs):
        self.slug = slugify(translit(
            '{0} : {1} : {2}'.format(self.position_objects.organizations_objects.name, self.position_objects.name,
                                     self.name), 'ru', reversed=True))
        super(Сabinet, self).save()

    def __str__(self):
        return '{0} : {1} : {2}'.format(self.position_objects.organizations_objects.name, self.position_objects.name,
                                        self.name)

    class Meta:
        verbose_name = 'Шкаф'
        verbose_name_plural = 'Шкафы'
        ordering = ['name']
