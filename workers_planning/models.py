from django.db import models
from django.utils import timezone
from transliterate import translit
from django.template.defaultfilters import slugify

from projects.models import Organizations_Objects
from workers.models import User


class Information_Missing(models.Model):
    """Причины отсутсвия на работе."""
    name = models.CharField(max_length=150, unique=False, null=False, blank=False, verbose_name='Причина отсутствия')
    color = models.CharField(max_length=7, default="#ffffff", verbose_name='Цвет')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='slug')

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        self.slug = slugify(translit(self.name, 'ru', reversed=True))
        super(Information_Missing, self).save()

    # def colored_name(self):
    #     return format_html(
    #         '<span style="color: #{};">{}</span>', self.color, )

    class Meta:
        verbose_name = 'Причина отсутствия'
        verbose_name_plural = 'Причины отсутствия'  # Во множественнмо числе
        ordering = ['name']  # Сортировка по каким полям, - обратная сортировка


class Information_Schedule(models.Model):
    """Информация о выходных днях и празднках"""
    date = models.DateField(unique=True, verbose_name='Дата')
    description = models.CharField(max_length=255, verbose_name='Описание')
    work = models.BooleanField(default=False, verbose_name='Выходим на работу')
    work_time = models.CharField(max_length=10, blank=True, verbose_name='Время работы')

    def __str__(self):
        return '{0}:{1}'.format(str(self.date), self.description)

    class Meta:
        verbose_name = 'Информация о выходных и праздниках'
        verbose_name_plural = 'Информация о выходных и праздниках'
        ordering = ['date']


class Workers_Missing(models.Model):
    """Отсутсвие сотрудников"""
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Сотрудник')
    information_missing = models.ForeignKey(Information_Missing, on_delete=models.PROTECT,
                                            verbose_name='Причина отсутствия')
    date_start = models.DateField(verbose_name='Дата начала отсутсвия')
    date_end = models.DateField(verbose_name='Дата окончание отсутсвия')
    comments = models.CharField(max_length=255, blank=True, verbose_name='Коментарии')

    def __str__(self):
        return '{0}:{1}:{2} - {3}'.format(self.user, self.information_missing, str(self.date_start), str(self.date_end))

    class Meta:
        verbose_name = 'Отсутсвие сотрудника'
        verbose_name_plural = 'Отсутсвие сотрудников'
        ordering = ['pk']


class Workers_Mission(models.Model):
    """Командировка сотрудников"""
    MISSING_STATUS = (
        ('final', 'Итоговая'),
        ('planning', 'Планируемая'),
    )
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Сотрудник')
    organizations_objects = models.ForeignKey(Organizations_Objects, on_delete=models.PROTECT,
                                              verbose_name='Объект командировки')
    date_departure = models.DateField(verbose_name='Дата выезда')
    date_start = models.DateField(blank=True, null=True, verbose_name='Дата начала работы')
    date_end = models.DateField(blank=True, null=True, verbose_name='Дата окончание работы')
    date_arrival = models.DateField(verbose_name='Дата прибытия')
    status = models.CharField(verbose_name='Статус', choices=MISSING_STATUS, max_length=30, default='final')

    def __str__(self):
        return '{0}:{1}:{2} - {3}'.format(self.user, self.organizations_objects, str(self.date_departure),
                                          str(self.date_arrival))

    class Meta:
        verbose_name = 'Командировка сотрудника'
        verbose_name_plural = 'Командировка сотрудников'
        ordering = ['pk']


def folder_report_file(instance, filename):
    file_name = "Табель.{0}.{1}:{2} {3}".format(instance.organizations_objects, instance.date_start, instance.date_end,
                                                ".pdf")
    print(file_name)
    return 'projects/{0}/{1}/report_File/{3}/{2}/{4}'.format(instance.organizations_objects.organization.pk,
                                                             instance.organizations_objects.pk,
                                                             instance.date_start.month,
                                                             instance.date_start.year, file_name)


class Workers_Mission_Report_File(models.Model):
    """Хранение табелей"""
    organizations_objects = models.ForeignKey(Organizations_Objects, on_delete=models.PROTECT,
                                              verbose_name='Название объекта')
    date_start = models.DateField(verbose_name='Дата начала в табеле')
    date_end = models.DateField(verbose_name='Дата окончания табеля')
    reviewer_protocol = models.FileField(upload_to=folder_report_file, verbose_name='Табель')
    date_load = models.DateTimeField(default=timezone.now, verbose_name='Дата добавления табеля')

    def __str__(self):
        return '{0}:{1} - {2}'.format(self.organizations_objects, self.date_start, self.date_end)

    class Meta:
        verbose_name = 'Табель'
        verbose_name_plural = 'Табеля'
        ordering = ['pk']


class Workers_Mission_Report(models.Model):
    """Табелирование сотрудников"""
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Сотрудник')
    user_mission = models.ForeignKey(Workers_Mission, on_delete=models.PROTECT, verbose_name='Командировка')
    user_mission_report_file = models.ForeignKey(Workers_Mission_Report_File, on_delete=models.PROTECT,
                                                 verbose_name='Табель')
    planning = models.TextField(verbose_name='Планирование работ', blank=True)
    report = models.TextField(verbose_name='Отчет о работе', blank=True)
    date_work = models.DateField(verbose_name='Дата выхода')
    hours_work = models.IntegerField(default=0, verbose_name='Часов работы')

    def __str__(self):
        return '{0}:{1}'.format(self.user, self.date_work)

    class Meta:
        verbose_name = 'Табелирования сотрудника'
        verbose_name_plural = 'Табелирование сотрудников'
        ordering = ['pk']


class Workers_Weekend_Work(models.Model):
    """Работа в выходные в офисе."""
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, verbose_name='Сотрудник')
    date = models.DateField(verbose_name='Дата выхода')
    planning = models.TextField(verbose_name='Планирование работ', blank=True)
    hours_working = models.FloatField(blank=True, default=-1.0, verbose_name='Отработанное время')

    def __str__(self):
        return '{0}:{1}'.format(str(self.date), self.user)

    class Meta:
        verbose_name = 'Работа в выходные в офисе.'
        verbose_name_plural = 'Работа в выходные в офисе.'
        ordering = ['pk']
