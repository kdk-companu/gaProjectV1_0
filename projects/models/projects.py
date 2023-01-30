from django.utils import timezone

from django.db import models
from django.urls import reverse
from transliterate import translit
from django.template.defaultfilters import slugify

from projects.models import Organization
from workers.models import Subdivision, Department
from workers.models import User


def objects_directory_path_files(instance, filename):
    # путь, куда будет осуществлена загрузка MEDIA_ROOT/user_<id>/<filename>
    return 'objects/{0}/documents/{1}'.format(instance.organizations_objects.slug, filename)


def сabinet_inspection_form_path_files(instance, filename):
    # путь, куда будет осуществлена загрузка MEDIA_ROOT/user_<id>/<filename>
    return 'objects/{0}/сabinet_inspection_form/{1}'.format(instance.organizations_objects.slug, filename)


def objects_position_path_files(instance, filename):
    # путь, куда будет осуществлена загрузка MEDIA_ROOT/user_<id>/<filename>
    return 'objects/{0}/position/{1}/{2}'.format(instance.objects_position.organizations_objects.slug,
                                                 instance.objects_position.slug, filename)


class Type_Document(models.Model):
    '''Типы докуменов'''
    name = models.CharField(max_length=255, unique=True, verbose_name='Название документа')
    cipher = models.CharField(max_length=255, unique=True, verbose_name='Шифр документа')
    description = models.TextField(verbose_name='Описание документа', blank=True)  # blank - пустое поле
    slug = models.SlugField(max_length=100, unique=True, db_index=True,
                            verbose_name='URL')  # unique - Уникальное,db_index - индексируемое

    def __str__(self):
        return self.cipher + " - " + self.name

    def save(self, **kwargs):
        slugSave = self.cipher + "_" + self.name
        self.slug = slugify(translit(slugSave, 'ru', reversed=True))
        super(Type_Document, self).save()

    # для создание ссылок. И использование ее в html
    def get_absolute_url(self):
        return reverse('type_document', kwargs={'type_document_slug': self.slug})

    class Meta:
        verbose_name = 'Название документа'
        verbose_name_plural = 'Название документов'  # Во множественнмо числе
        ordering = ['pk']  # Сортировка по каким полям, - обратная сортировка
        default_permissions = ('')


#######################################################

class Organizations_Objects(models.Model):
    '''Название объекта'''
    STATUS_CHOICES = (
        ('Done', 'Выполнено'),
        ('Not_done', 'Не выполнено'),
        ('Running', 'Выполняется'),
        ('Suspended', 'Приостановлено'),
    )
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name='Эксплуатирующая фирма')
    name = models.CharField(max_length=255, unique=True, verbose_name='Название объекта')
    name_tables = models.CharField(max_length=80, unique=True, blank=False, verbose_name='Название для табеля')
    short_names = models.CharField(max_length=80, unique=True, blank=True, verbose_name='Обиходные название')
    description = models.TextField(verbose_name='Описание объекта', blank=True)
    property_location = models.TextField(verbose_name='Расположение объекта. Транспорт.', blank=True)

    slug = models.SlugField(max_length=100, unique=True, db_index=True,
                            verbose_name='URL')  # unique - Уникальное,db_index - индексируемое

    def __str__(self):
        return self.organization.name + ". " + self.name

    def save(self, **kwargs):
        self.slug = slugify(translit(self.name, 'ru', reversed=True))
        super(Organizations_Objects, self).save()

    # для создание ссылок. И использование ее в html
    def get_absolute_url(self):
        return reverse('organizations_objects', kwargs={'organizations_objects_slug': self.slug})

    # Админка на русском языке
    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'  # Во множественнмо числе
        ordering = ['pk']  # Сортировка по каким полям, - обратная сортировка


class Organizations_Objects_Documents(models.Model):
    organizations_objects = models.ForeignKey(Organizations_Objects, on_delete=models.CASCADE, blank=False,
                                              verbose_name='Название объекта')
    type_document = models.ForeignKey(Type_Document, on_delete=models.CASCADE,
                                      verbose_name='Тип документа')
    description = models.TextField(verbose_name='Описание документа', blank=True)  # blank - пустое поле
    document = models.FileField(upload_to=objects_directory_path_files, verbose_name='Документ', null=True,
                                blank=True)
    date_joined = models.DateTimeField(default=timezone.now)

    slug = models.SlugField(max_length=150, unique=True, db_index=True,
                            verbose_name='URL')  # unique - Уникальное,db_index - индексируемое

    def __str__(self):
        return self.organizations_objects.name + ". " + self.type_document.cipher + " - " + self.type_document.name + "(" + str(
            self.date_joined) + ")"

    def save(self, **kwargs):
        slugSave = self.organizations_objects.name + "_" + self.type_document.name + "_" + str(self.date_joined)
        self.slug = slugify(translit(slugSave, 'ru', reversed=True))
        super(Organizations_Objects_Documents, self).save()

    # для создание ссылок. И использование ее в html
    def get_absolute_url(self):
        return reverse('organizations_objects_document', kwargs={'organizations_objects_document_slug': self.slug})

    class Meta:
        verbose_name = 'Объект. Документ'
        verbose_name_plural = 'Объект. Документы'  # Во множественнмо числе
        ordering = ['date_joined']  # Сортировка по каким полям, - обратная сортировка
        default_permissions = ('')


class Objects_Position(models.Model):
    '''Позиция для установки шкафа'''
    PROJECT_STAGE = (
        ('Factory_acceptance', 'Заводская приемка'),
        ('Waiting_for_setup', 'Ожидание наладки'),
        ('Commissioning', 'Пусконаладочные работы'),
        ('Experimental_exploitation', 'Опытная эксплатация'),
        ('Completed_project', 'Законченный проект'),
    )
    organizations_objects = models.ForeignKey(Organizations_Objects, on_delete=models.CASCADE,
                                              verbose_name='Название объекта')
    name = models.CharField(max_length=255, unique=True, verbose_name='Позиция')
    short_names = models.CharField(max_length=80, unique=True, blank=True, verbose_name='Обиходные название')
    description = models.TextField(verbose_name='Описание позиции', blank=True)  # blank - пустое поле
    subdivision = models.ForeignKey(Subdivision, on_delete=models.CASCADE,
                                    verbose_name='Задание на управлении')
    department = models.ForeignKey(Department, on_delete=models.CASCADE,
                                   verbose_name='Задание на отделе')
    сhecking_cabinet = models.ManyToManyField(User, blank=True, verbose_name='Проверяющие шкаф')

    сabinet_inspection_form = models.FileField(upload_to=сabinet_inspection_form_path_files,
                                               verbose_name='Бланк проверки шкафа', null=True,
                                               blank=True)
    # Добавить статусы на систему
    stage = models.CharField(verbose_name='Состояние проекта', choices=PROJECT_STAGE, max_length=50,
                             default='Factory_acceptance')

    slug = models.SlugField(max_length=100, unique=True, db_index=True,
                            verbose_name='URL')  # unique - Уникальное,db_index - индексируемое

    def __str__(self):
        return self.organizations_objects.name + ". " + self.name

    def save(self, **kwargs):
        slugSave = self.organizations_objects.name + "_" + self.name
        self.slug = slugify(translit(slugSave, 'ru', reversed=True))
        super(Objects_Position, self).save()

    # для создание ссылок. И использование ее в html
    def get_absolute_url(self):
        return reverse('objects_position', kwargs={'objects_position_slug': self.slug})

    class Meta:
        verbose_name = 'Позиция'
        verbose_name_plural = 'Позиции'  # Во множественнмо числе
        ordering = ['pk']  # Сортировка по каким полям, - обратная сортировка
        default_permissions = ('')


class Objects_Position_Documents(models.Model):
    objects_position = models.ForeignKey(Objects_Position, on_delete=models.CASCADE, blank=False,
                                         verbose_name='Позиция')
    type_document = models.ForeignKey(Type_Document, on_delete=models.CASCADE,
                                      verbose_name='Тип документа')
    description = models.TextField(verbose_name='Описание документа', blank=True)  # blank - пустое поле
    document = models.FileField(upload_to=objects_position_path_files, verbose_name='Документ', null=True,
                                blank=True)
    date_joined = models.DateTimeField(default=timezone.now)

    slug = models.SlugField(max_length=150, unique=True, db_index=True,
                            verbose_name='URL')  # unique - Уникальное,db_index - индексируемое

    def __str__(self):
        return self.objects_position.name + ". " + self.type_document.cipher + " - " + self.type_document.name + "(" + str(
            self.date_joined) + ")"

    def save(self, **kwargs):
        slugSave = self.objects_position.name + "_" + self.type_document.name + "_" + str(self.date_joined)
        self.slug = slugify(translit(slugSave, 'ru', reversed=True))
        super(Objects_Position_Documents, self).save()

    # для создание ссылок. И использование ее в html
    def get_absolute_url(self):
        return reverse('objects_position_documents', kwargs={'objects_position_documents_slug': self.slug})

    class Meta:
        verbose_name = 'Позиция. Документ'
        verbose_name_plural = 'Позиция. Документы'  # Во множественнмо числе
        ordering = ['date_joined']  # Сортировка по каким полям, - обратная сортировка
        default_permissions = ('')


#########################################################
class Produced_Сabinets(models.Model):
    objects_position = models.ForeignKey(Objects_Position, on_delete=models.CASCADE, blank=False,
                                         verbose_name='Позиция')
    name = models.CharField(max_length=100, unique=False, verbose_name='Название')
    factory_number = models.CharField(max_length=100, unique=True, verbose_name='Заводской номер')
    сabinet_сonstructor = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name='user1',
                                            verbose_name='Конструктор')
    сabinet_builder = models.ManyToManyField(User, related_name='user2', blank=True, verbose_name='Сборщик')
    сomments = models.TextField(blank=True, verbose_name='Коментарии')
    slug = models.SlugField(max_length=150, unique=True, db_index=True,
                            verbose_name='URL')  # unique - Уникальное,db_index - индексируемое

    def __str__(self):
        return self.factory_number

    def save(self, **kwargs):
        self.slug = slugify(translit(self.factory_number, 'ru', reversed=True))
        super(Produced_Сabinets, self).save()

    # для создание ссылок. И использование ее в html
    def get_absolute_url(self):
        return reverse('produced_cabinets', kwargs={'produced_cabinets_slug': self.slug})

    class Meta:
        verbose_name = 'Шкаф'
        verbose_name_plural = 'Шкафы'  # Во множественнмо числе
        ordering = ['factory_number']  # Сортировка по каким полям, - обратная сортировка
        default_permissions = ('')


class Development_Task(models.Model):
    '''Задание на разработку'''
    STATUS_COMPLETION_CHOICES = (
        ('Done', 'Выполнено'),
        ('Not_done', 'Не выполнено'),
        ('Running', 'Выполняется'),
        ('Suspended', 'Приостановлено'),
    )
    POSITION_STATUS_CHOICES = (
        ('New_Object', 'Новый объект'),
        ('Overhaul', 'Капитальный ремонт'),
        ('Reconstruction', 'Реконструкция'),
    )
    tasks_ppo = models.CharField(max_length=60, unique=True, verbose_name='Задания на ППО')
    name_systems = models.CharField(max_length=250, unique=False, verbose_name='Название системы')
    status_systems = models.CharField(verbose_name='Статус системы', choices=POSITION_STATUS_CHOICES, max_length=50,
                                      default='New_Object')
    customer = models.ForeignKey(Organization, on_delete=models.PROTECT, blank=False,
                                 null=True, related_name='organization1', verbose_name='Заказчик')
    exploitation = models.ForeignKey(Organization, on_delete=models.PROTECT, blank=False,
                                     null=True, related_name='organization2', verbose_name='Эксплуатация')
    designer = models.ForeignKey(Organization, on_delete=models.PROTECT, blank=False,
                                 null=True, related_name='organization3', verbose_name='Проектировщик')
    organizations_objects = models.ForeignKey(Organizations_Objects, on_delete=models.PROTECT, blank=False,
                                              null=True, verbose_name='Объект')
    objects_position = models.OneToOneField(Objects_Position, on_delete=models.PROTECT, blank=False,
                                            null=True, verbose_name='Позиция')
    gip = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Ф.И.О. ГИПа')
    task = models.TextField(verbose_name='Описание задания')
    part_equipment = models.TextField(verbose_name='Состав оборудования')
    status = models.CharField(verbose_name='Отметка выполнения', choices=STATUS_COMPLETION_CHOICES, max_length=50,
                              default='Not_done')
    date_software_development_planned = models.DateField(verbose_name='Разработка ППО. Планируемая.', null=True,
                                                         blank=True)
    date_software_development_actual = models.DateField(verbose_name='Разработка ППО. Фактическая.', null=True,
                                                        blank=True)
    date_documentation_development_planned = models.DateField(verbose_name='Разработка документации. Планируемая.',
                                                              null=True, blank=True)
    date_documentation_development_actual = models.DateField(verbose_name='Разработка документации. Фактическая.',
                                                             null=True, blank=True)
    date_factory_acceptance_planned = models.DateField(verbose_name='Заводская приемка. Планируемая.',
                                                       null=True, blank=True)
    date_factory_acceptance_actual = models.DateField(verbose_name='Заводская приемка. Фактическая.',
                                                      null=True, blank=True)
    date_shipment_equipment_planned = models.DateField(verbose_name='Отгрузка оборудования. Планируемая.',
                                                       null=True, blank=True)
    date_shipment_equipment_actual = models.DateField(verbose_name='Отгрузка оборудования. Фактическая.',
                                                      null=True, blank=True)
    source_data_folder = models.CharField(max_length=255, unique=False, verbose_name='Папка с исходными данными')

    date_issue = models.DateTimeField(default=timezone.now, verbose_name='Дата регистрации задания.')
    slug = models.SlugField(max_length=150, unique=True, db_index=True,
                            verbose_name='URL')  # unique - Уникальное,db_index - индексируемое

    def save(self, **kwargs):
        self.slug = slugify(translit(self.tasks_ppo, 'ru', reversed=True))
        super(Development_Task, self).save()

    def __str__(self):
        return self.tasks_ppo + ". " + self.name_systems

    # для создание ссылок. И использование ее в html
    def get_absolute_url(self):
        return reverse('development_task_view', kwargs={'development_task_slug': self.slug})

    class Meta:
        verbose_name = 'Задание на разработку'
        verbose_name_plural = 'Задание на разработки'  # Во множественнмо числе
        ordering = ['date_issue']  # Сортировка по каким полям, - обратная сортировка
        default_permissions = ('')
