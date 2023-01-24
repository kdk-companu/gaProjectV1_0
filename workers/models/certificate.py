# import os
# import datetime
# from django.db.models.signals import post_save, post_delete
# from django.urls import reverse
# from changelog_workers.soft.mixins import ChangeloggableMixin
# from django.db import models
# from django.template.defaultfilters import slugify
# from transliterate import translit
# from changelog_workers.soft.signals import journal_delete_handler, journal_save_handler
# from workers.models import User, Chief
#
#
# class Сertificates(ChangeloggableMixin, models.Model):
#     '''Разновидность сертификатов'''
#     name = models.CharField(max_length=150, unique=True, verbose_name='Название сертификата')
#     abbreviation = models.CharField(max_length=100, unique=True, verbose_name='Сокращенное название')
#     how_to_take = models.TextField(null=True, verbose_name='Как сдавать')
#     answers = models.TextField(null=True, verbose_name='Ответы')
#     state = models.BooleanField(default=True, verbose_name='Актуальность')
#     slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='URL')
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = 'Сертификат'
#         verbose_name_plural = 'Сертификаты'
#         ordering = ['pk']
#         default_permissions = ('')
#         permissions = (
#             ('certificates_view', 'Сертификаты. Просмотр.'),
#             ('certificates_change', 'Сертификаты. Редактирование.'),
#             ('certificates_delete', 'Сертификаты. Удаление.'),
#             ('certificates_add', 'Сертификаты. Добавить.'),
#         )
#
#     def save(self, **kwargs):
#         self.slug = slugify(translit(self.abbreviation, 'ru', reversed=True))
#         super(Сertificates, self).save()
#
#     def get_absolute_url(self):
#         return reverse('certificates_update', kwargs={'сertificates_slug': self.slug})
#
#
# class Сertificate_Parts(ChangeloggableMixin, models.Model):
#     '''Части сертификатов'''
#     certificates = models.ForeignKey(Сertificates, on_delete=models.CASCADE, blank=True, verbose_name='Сертификаты')
#     name = models.CharField(max_length=150, unique=True, verbose_name='Название части')
#     validity = models.IntegerField(default=0, unique=False, verbose_name='Срок годности месяцев')
#     change_chief = models.BooleanField(default=False, verbose_name='Не актуальность при смене должности')
#     state = models.BooleanField(default=True, verbose_name='Актуальность')
#     slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='URL')
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = 'Сертификат части'
#         verbose_name_plural = 'Сертификаты части'
#         ordering = ['pk']
#         default_permissions = ('')
#
#         permissions = (
#             ('certificate_parts_view', 'Сертификаты части. Просмотр.'),
#             ('certificate_parts_change', 'Сертификаты части. Редактирование.'),
#             ('certificate_parts_delete', 'Сертификаты части. Удаление.'),
#             ('certificate_parts_add', 'Сертификаты части. Добавить.'),
#         )
#
#     def save(self, **kwargs):
#         self.slug = slugify(translit(self.name, 'ru', reversed=True))
#         super(Сertificate_Parts, self).save()
#
#     def get_absolute_url(self):
#         return reverse('certificates_parts_update', kwargs={'сertificates_parts_slug': self.slug})
#
#
# def user_directory_certificate1(instance, filename):
#     upload_to = str('user/{0}/certificate/'.format(instance.user.pk))
#     ext = filename.split('.')[-1]
#     filename = '{}.{}'.format(str(datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S')) + 'file1', ext)
#     return os.path.join(upload_to, filename)
#
#
# def user_directory_certificate2(instance, filename):
#     upload_to = str('user/{0}/certificate/'.format(instance.user.pk))
#     ext = filename.split('.')[-1]
#     filename = '{}.{}'.format(str(datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S')) + 'file2', ext)
#     return os.path.join(upload_to, filename)
#
#
# def user_directory_certificate3(instance, filename):
#     upload_to = str('user/{0}/certificate/'.format(instance.user.pk))
#     ext = filename.split('.')[-1]
#     filename = '{}.{}'.format(str(datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S')) + 'file3', ext)
#     return os.path.join(upload_to, filename)
#
#
# class Сertificate_Users(ChangeloggableMixin, models.Model):
#     '''Сертификаты добавленные пользователями'''
#     certificate = models.ForeignKey(Сertificate_Parts, on_delete=models.CASCADE, null=True,
#                                     verbose_name='Сертификаты часть')
#     user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='ФИО')
#     date_delivery = models.DateField(verbose_name='Дата начала действия сертификата', null=False, blank=True)
#     chief = models.ForeignKey(Chief, on_delete=models.PROTECT, blank=True, null=False, verbose_name='Должность')
#     file1 = models.FileField(upload_to=user_directory_certificate1, verbose_name='Скан №1', null=True, blank=True)
#     file2 = models.FileField(upload_to=user_directory_certificate2, verbose_name='Скан №2', null=True, blank=True)
#     file3 = models.FileField(upload_to=user_directory_certificate3, verbose_name='Скан №3', null=True, blank=True)
#
#     def __str__(self):
#         return str(self.user) + ' : ' + str(self.certificate) + ' : ' + str(self.date_delivery)
#
#     class Meta:
#         verbose_name = 'Сертификат работника'
#         verbose_name_plural = 'Сертификаты работников'
#         ordering = ['pk']
#         default_permissions = ('')
#
#         permissions = (
#             ('certificate_users_view', 'Сертификаты сотрудников. Просмотр.'),
#             ('certificate_users_change', 'Сертификаты сотрудников. Редактирование.'),
#             ('certificate_users_delete', 'Сертификаты сотрудников. Удаление.'),
#             ('certificate_users_add', 'Сертификаты сотрудников. Добавить.'),
#
#             ('certificate_users_change_superiors', 'Сертификаты сотрудников. Редактирование. Руководство.'),
#             ('certificate_users_delete_superiors', 'Сертификаты сотрудников. Удаление. Руководство.'),
#             ('certificate_users_add_superiors', 'Сертификаты сотрудников. Добавить. Руководство.'),
#         )
#
#
# post_save.connect(journal_save_handler, sender=Сertificates)
# post_delete.connect(journal_delete_handler, sender=Сertificates)
#
# post_save.connect(journal_save_handler, sender=Сertificate_Parts)
# post_delete.connect(journal_delete_handler, sender=Сertificate_Parts)
#
# post_save.connect(journal_save_handler, sender=Сertificate_Users)
# post_delete.connect(journal_delete_handler, sender=Сertificate_Users)
