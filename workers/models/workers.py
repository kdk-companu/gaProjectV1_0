import os
from uuid import uuid4

from PIL import Image
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from transliterate import translit

from changelog_workers.soft.mixins import ChangeloggableMixin
from changelog_workers.soft.signals import journal_save_handler, journal_delete_handler
from workers.models import Subdivision, Department, Chief
from workers.models.managers import UserManager


def workers_image_path(instance, filename):
    '''путь, куда будет осуществлена загрузка MEDIA_ROOT/user_<id>/<filename>'''
    return 'user/{0}/images/{1}'.format(instance.slug, filename)


class User(ChangeloggableMixin, AbstractBaseUser, PermissionsMixin):
    '''Сотрудники переписанная от User'''

    '''https://docs.djangoproject.com/en/4.1/ref/models/instances/'''

    WORKERS_STATUS = (
        ('employee', 'Сотрудник'),
        ('fired', 'Уволен'),
    )
    # ФИО
    surname = models.CharField(max_length=60, unique=False, verbose_name='Фамилия')
    name = models.CharField(max_length=60, unique=False, verbose_name='Имя')
    patronymic = models.CharField(max_length=60, unique=False, verbose_name='Отчество')
    slug = models.SlugField(max_length=100, unique=True, db_index=True,
                            verbose_name='slug')  # unique - Уникальное,db_index - индексируемое
    # Контакты
    phone = PhoneNumberField(null=False, blank=False, unique=True, verbose_name='Телефон')
    email = models.EmailField(unique=False, verbose_name='Электронная почта')
    # Место работы
    subdivision = models.ForeignKey(Subdivision, on_delete=models.PROTECT, blank=True,
                                    null=True, verbose_name='Управление фактически')
    department = models.ForeignKey(Department, on_delete=models.PROTECT, blank=True,
                                   null=True, verbose_name='Отдел фактически')
    chief = models.ForeignKey(Chief, on_delete=models.PROTECT, blank=True,
                              null=True, verbose_name='Должность')
    # Текущий статус работника
    employee = models.CharField(verbose_name='Сотрудник', choices=WORKERS_STATUS, max_length=30, default='employee')
    employee_date = models.DateField(verbose_name='Дата увольнения', null=True, blank=True)
    # Аватарки
    image = models.ImageField(upload_to=workers_image_path, null=True, blank=True, verbose_name='Фото')
    image_smol = models.ImageField(upload_to=workers_image_path, null=True, blank=True, verbose_name='Фото')
    # Система прав
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['surname', 'name', 'patronymic']
    objects = UserManager()

    def __str__(self):
        return self.surname + " " + self.name + " " + self.patronymic

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'  # Во множественнмо числе
        ordering = ['chief']  # Сортировка по каким полям, - обратная сортировка
        default_permissions = ('')

        permissions = (
            ('workers_view', 'Просмотр страницы пользователя.'),
            ('workers_change_image', 'Редактировать фотографию.'),
            ('workers_change_contact', 'Редактировать контакты.'),

            ('workers_view_superiors', 'Просмотр страницы пользователя. Руководство.'),
            ('workers_update_password_superiors', 'Обновление пароля. Руководство.'),
            ('workers_add_superiors', 'Добавить пользователя. Руководство.'),
            ('workers_change_image_superiors', 'Редактировать фотографию. Руководство.'),
            ('workers_change_contact_superiors', 'Редактировать контакты. Руководство.'),
        )

    def save(self, *args, **kwargs):
        # Создаем slug
        slug_name = self.surname + "" + self.name + "" + self.patronymic
        self.slug = slugify(translit(slug_name, 'ru', reversed=True))

        # Сохранение фотографий
        if self.image:
            # Полный путь к папкам
            folder_user = "media/user/" + str(self.pk)
            folder_save = "media/user/" + str(self.pk) + "/images/"
            url_save = "user/" + str(self.pk) + "/images/"
            # Создание папок
            if not os.path.isdir(folder_user):
                os.mkdir(folder_user)
            if not os.path.isdir(folder_save):
                os.mkdir(folder_save)
            # Обработка изображнеий
            img = Image.open(self.image)
            width = self.image.width
            height = self.image.height
            min_size = min(width, height)
            # Обрезка картинки до квадрата
            img = img.crop((0, 0, min_size, min_size))
            # Первое уменьшение
            oputput_size = (300, 300)
            img.thumbnail(oputput_size)
            img.save(folder_save + "photo.jpg")
            self.image = url_save + "photo.jpg"
            # Второе уменьшение
            oputput_size = (128, 128)
            img.thumbnail(oputput_size)
            img.save(folder_save + "smol_photo.jpg")
            self.image_smol = url_save + "smol_photo.jpg"

        super().save()

    def get_absolute_url(self):
        return reverse('workers_views', kwargs={'workers_slug': self.slug})

    def get_absolute_url_image(self):
        return reverse('workers_image', kwargs={'workers_slug': self.slug})

    def get_absolute_url_edit(self):
        return reverse('workers_update', kwargs={'workers_slug': self.slug})

    def get_absolute_url_basic_edit(self):
        return reverse('workers_basic_update', kwargs={'workers_slug': self.slug})

    def get_absolute_url_closed_edit(self):
        return reverse('workers_closed_update', kwargs={'workers_slug': self.slug})

    def get_absolute_url_update_pass(self):
        return reverse('workers_update_password', kwargs={'workers_slug': self.slug})

    def get_absolute_url_passport(self):
        return reverse('workers_passport', kwargs={'workers_slug': self.slug})

    def get_absolute_url_inn(self):
        return reverse('workers_inn', kwargs={'workers_slug': self.slug})

    def get_absolute_url_snils(self):
        return reverse('workers_snils', kwargs={'workers_slug': self.slug})

    def get_absolute_url_archive(self):
        return reverse('workers_archive', kwargs={'workers_slug': self.slug})

    def get_absolute_url_signature(self):
        return reverse('workers_signature', kwargs={'workers_slug': self.slug})

    def get_absolute_url_certificate(self):
        return reverse('workers_certificate_add', kwargs={'workers_slug': self.slug})

    def get_absolute_url_contacts(self):
        return reverse('contacts_edit', kwargs={'workers_slug': self.slug})


class User_Basic_Information(ChangeloggableMixin, models.Model):
    '''Базовая информация о сотрудниках'''
    GENDER_CHOICES = (
        ('Male', 'Мужской'),
        ('Female', 'Женский'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='ФИО')
    subdivision_in_company = models.ForeignKey(Subdivision, on_delete=models.PROTECT, blank=True,
                                               null=True, verbose_name='Управление официально')
    department_in_company = models.ForeignKey(Department, on_delete=models.PROTECT, blank=True,
                                              null=True, verbose_name='Отдел официально')
    date_employment = models.DateField(verbose_name='Дата трудоустройства', null=True, blank=True)
    date_chief = models.DateField(verbose_name='Дата в должности', null=True, blank=True)
    number_ga = models.IntegerField(default=0, verbose_name='Номер табеля', null=True, blank=True)
    date_birth = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    email_home = models.EmailField(max_length=255, unique=False, null=True, blank=True, verbose_name='Личная почта')
    phone_additional1 = PhoneNumberField(null=True, blank=True, unique=False, verbose_name='Телефон дополнительный №1')
    phone_additional2 = PhoneNumberField(null=True, blank=True, unique=False, verbose_name='Телефон дополнительный №2')
    home_address = models.CharField(max_length=255, verbose_name='Домашний адрес', null=True, blank=True)
    home_metro = models.CharField(max_length=255, verbose_name='Ближайшее метро', null=True, blank=True)
    gender = models.CharField(verbose_name='Пол', choices=GENDER_CHOICES, max_length=10, blank=True)

    def __str__(self):
        return self.user.surname + " " + self.user.name + " " + self.user.patronymic

    class Meta:
        verbose_name = 'Сотрудники общая информация'
        verbose_name_plural = 'Сотрудники общая информация'  # Во множественнмо числе
        ordering = ['pk']  # Сортировка по каким полям, - обратная сортировка
        default_permissions = ('')
        permissions = (
            ('user_basic_change', 'Базовая информация. Изменение.'),
            ('user_basic_views', 'Базовая информация. Просмотр.'),

            ('user_basic_change_superiors', 'Базовая информация. Изменение. Руководство.'),
            ('user_basic_views_superiors', 'Базовая информация. Просмотр.Руководство.'),
        )

    # При создании пользователя данная таблица создается автоматом
    @receiver(post_save, sender=User)
    def create_user_base_information(sender, instance, created, **kwargs):
        if created:
            User_Basic_Information.objects.create(user=instance)


def user_directory_path_files(instance, filename):
    # путь, куда будет осуществлена загрузка MEDIA_ROOT/user_<id>/<filename>
    return 'user/{0}/files/{1}'.format(instance.user.slug, filename)


def user_directory_path_save(instance, filename):
    upload_to = str('user/{0}/files/'.format(instance.user.pk))
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, ext)
    return os.path.join(upload_to, filename)


class User_Closed_Information(ChangeloggableMixin, models.Model):
    '''Закрытая информация о сотрудники'''
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='ФИО')
    organization_order_of_employment = models.CharField(max_length=255, verbose_name='Приказ о трудоустройстве',
                                                        null=True, blank=True)
    organization_labor_contract = models.CharField(max_length=255, verbose_name='Трудовой договор', null=True,
                                                   blank=True)
    passport_serial = models.IntegerField(default=0, verbose_name='Паспорт Серия', null=True, blank=True)
    passport_number = models.IntegerField(default=0, verbose_name='Паспорт Номер', null=True, blank=True)
    passport_passport_issued = models.CharField(max_length=255, verbose_name='Паспорт Выдан', null=True, blank=True)
    passport_passport_issued_date = models.DateField(verbose_name='Паспорт Дата выдачи', null=True, blank=True)
    passport_place_of_issue = models.CharField(max_length=255, verbose_name='Паспорт Код подразделения', null=True,
                                               blank=True)
    passport_registration = models.CharField(max_length=255, verbose_name='Паспорт Место выдачи', null=True, blank=True)
    passport_of_residence = models.CharField(max_length=255, verbose_name='Паспорт Место жительства', null=True,
                                             blank=True)
    passport_scan = models.FileField(upload_to=user_directory_path_save, verbose_name='Паспорт скан', null=True,
                                     blank=True)
    snils_number = models.CharField(max_length=255, verbose_name='СНИЛС номер', null=True,
                                    blank=True)
    snils_scan = models.FileField(upload_to=user_directory_path_save, verbose_name='СНИЛС скан', null=True,
                                  blank=True)
    inn_number = models.CharField(max_length=255, verbose_name='Инн номер', null=True,
                                  blank=True)
    inn_scan = models.FileField(upload_to=user_directory_path_save, verbose_name='Инн скан', null=True,
                                blank=True)
    archive_documents_employment = models.FileField(upload_to=user_directory_path_save,
                                                    verbose_name='Пакет документов при трудоустройстве',
                                                    null=True, blank=True)

    signature_example = models.ImageField(upload_to=user_directory_path_files, verbose_name='Пример подписи', null=True,
                                          blank=True)

    def __str__(self):
        return self.user.surname + " " + self.user.name + " " + self.user.patronymic

    class Meta:
        verbose_name = 'Сотрудники закрытая информация'
        verbose_name_plural = 'Сотрудники закрытая информация'  # Во множественнмо числе
        ordering = ['pk']  # Сортировка по каким полям, - обратная сортировкаа
        default_permissions = ('')
        permissions = (
            ('user_basic_views', 'Закрытая инфомрация. Просмотр.'),

            ('user_basic_add_passport_superiors', 'Закрытая инфомрация. Редактирование. Паспорт. Руководство.'),
            ('user_basic_views_passport_superiors', 'Закрытая инфомрация. Просмотр. Паспорт. Руководство.'),

            ('user_basic_add_snils_superiors', 'Закрытая инфомрация. Редактирование. СНИЛС. Руководство.'),
            ('user_basic_views_snils_superiors', 'Закрытая инфомрация. Просмотр. СНИЛС. Руководство.'),

            ('user_basic_add_inn_superiors', 'Закрытая инфомрация. Редактирование. ИНН. Руководство.'),
            ('user_basic_views_inn_superiors', 'Закрытая инфомрация. Просмотр. ИНН. Руководство.'),

            ('user_basic_add_signature_superiors', 'Закрытая инфомрация. Редактирование. Подпись. Руководство.'),
            ('user_basic_views_signature_superiors', 'Закрытая инфомрация. Просмотр. Подпись. Руководство.'),

            ('user_basic_add_archive_superiors',
             'Закрытая инфомрация. Редактирование. Архив при трудоустройстве. Руководство.'),
            ('user_basic_views_archive_superiors',
             'Закрытая инфомрация. Просмотр. Архив при трудоустройстве. Руководство.'),

            ('user_basic_views_superiors', 'Закрытая инфомрация. Просмотр. Руководство.'),
            ('user_basic_change_superiors', 'Закрытая инфомрация. Изменение. Руководство. Руководство.'),
        )

    # При создании пользователя данная таблица создается автоматом
    @receiver(post_save, sender=User)
    def create_user_closed_information(sender, instance, created, **kwargs):
        if created:
            User_Closed_Information.objects.create(user=instance)

    def save(self, *args, **kwargs):
        # Загрузка образца подписи
        if self.signature_example and not '/' in str(self.signature_example):
            try:
                file_remove = User_Closed_Information.objects.get(user__slug=self.user.slug)
                file_remove.signature_example.delete(save=False)
            except:
                pass
            # Полный путь к папкам
            folder_user = "media/user/" + str(self.user.pk)
            folder_save = "media/user/" + str(self.user.pk) + "/files/"
            url_save = "user/" + str(self.user.pk) + "/files/"
            # Создание папок
            if not os.path.isdir(folder_user):
                os.mkdir(folder_user)
            if not os.path.isdir(folder_save):
                os.mkdir(folder_save)
            # Обработка изображнеий
            img = Image.open(self.signature_example)
            width = img.size[0]
            height = img.size[1]
            max_size = max(width, height)
            # Обрезка картинки до квадрата
            img = img.crop((0, 0, 700, 350))
            # Первое уменьшение
            name_file = uuid4().hex + ".png"
            img.save(folder_save + name_file)
            self.signature_example = url_save + name_file
        # Загрузка паспорта
        if self.passport_scan and not '/' in str(self.passport_scan):
            try:
                passport_remove = User_Closed_Information.objects.get(user__slug=self.user.slug)
                passport_remove.passport_scan.delete(save=False)
            except:
                pass
        if self.inn_scan and not '/' in str(self.inn_scan):
            try:
                inn_remove = User_Closed_Information.objects.get(user__slug=self.user.slug)
                inn_remove.inn_scan.delete(save=False)
            except:
                pass
        if self.snils_scan and not '/' in str(self.snils_scan):
            try:
                snils_remove = User_Closed_Information.objects.get(user__slug=self.user.slug)
                snils_remove.snils_scan.delete(save=False)
            except:
                pass
        if self.archive_documents_employment and not '/' in str(self.archive_documents_employment):
            try:
                archive_documents_employment_remove = User_Closed_Information.objects.get(user__slug=self.user.slug)
                archive_documents_employment_remove.archive_documents_employment.delete(save=False)
            except:
                pass

        super().save()


# Логирование
post_save.connect(journal_save_handler, sender=User)
post_delete.connect(journal_delete_handler, sender=User)

post_save.connect(journal_save_handler, sender=User_Basic_Information)
post_delete.connect(journal_delete_handler, sender=User_Basic_Information)

post_save.connect(journal_save_handler, sender=User_Closed_Information)
post_delete.connect(journal_delete_handler, sender=User_Closed_Information)
