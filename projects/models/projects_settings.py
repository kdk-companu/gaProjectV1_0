from django.db import models
from django.urls import reverse
from transliterate import translit
from django.template.defaultfilters import slugify

from workers.models import User, Department


class Organization_Direction(models.Model):
    '''Направление деятельности организации'''
    name = models.CharField(max_length=255, unique=True, verbose_name='Направление дейтельности организации')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Направление дейтельности организации'
        verbose_name_plural = 'Направление дейтельности организаций'
        ordering = ['name']

    def save(self, **kwargs):
        self.slug = slugify(translit(self.name, 'ru', reversed=True))
        super(Organization_Direction, self).save()

    def get_absolute_url(self):
        return reverse('organization_direction_edit', kwargs={'organization_direction_slug': self.slug})


class Organization(models.Model):
    '''Организация'''
    name = models.CharField(max_length=255, unique=True, verbose_name='Организация')
    organization_direction = models.ForeignKey(Organization_Direction, on_delete=models.PROTECT, blank=False, null=True,
                                               verbose_name='Направление деятельности организация')
    site = models.URLField(max_length=255, unique=False, blank=True, verbose_name='Сайт')
    description = models.TextField(verbose_name='Описание фирмы', blank=True)
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'
        ordering = ['pk']

    def save(self, **kwargs):
        self.slug = slugify(translit(self.name, 'ru', reversed=True))
        super(Organization, self).save()

    def get_absolute_url(self):
        return reverse('organization_edit', kwargs={'organization_slug': self.slug})


class Type_Document(models.Model):
    '''Типы докуменов разрабатываемых документов'''
    SYSTEM_CHOICES = (
        ('ACS', 'САУ'),
        ('COMPLETELY_ACS', 'Комплектно поставляемые САУ'),
    )
    STAGE_CHOICES = (
        ('WORKING', 'Рабочая'),
        ('OPERATIONAL', 'Эксплуатационная'),
        ('COMPLETELY_ACS', ' - '),
    )
    system = models.CharField(verbose_name='Система', choices=SYSTEM_CHOICES, max_length=100, default='ACS')
    stage = models.CharField(verbose_name='Этап документации', choices=STAGE_CHOICES, max_length=100, default='ACS')
    name = models.CharField(max_length=255, verbose_name='Наименования документа')
    сode_document = models.CharField(max_length=50, blank=True, verbose_name='Код ЭД')
    additional_instructions = models.TextField(verbose_name='Дополнительные указания', blank=True)
    basic_documents = models.BooleanField(default=False, verbose_name='Базовый документ')
    developers = models.ManyToManyField(Department, verbose_name='Отделы')
    sorted = models.IntegerField(default=0, verbose_name='Порядок документов')
    slug = models.SlugField(max_length=100, unique=True, db_index=True,
                            verbose_name='URL')  # unique - Уникальное,db_index - индексируемое

    def __str__(self):
        return self.system + " - " + self.сode_document + " - " + self.name

    def save(self, **kwargs):
        slugSave = self.system + " - " + self.сode_document + " - " + self.name
        self.slug = slugify(translit(slugSave, 'ru', reversed=True))
        super(Type_Document, self).save()

    def get_absolute_url(self):
        return reverse('type_document_edit', kwargs={'type_document_slug': self.slug})

    class Meta:
        verbose_name = 'Разрабатываемый документ'
        verbose_name_plural = 'Разрабатываемые документы'  # Во множественнмо числе
        ordering = ['pk']  # Сортировка по каким полям, - обратная сортировка
        default_permissions = ('')
