from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import FileField


class Letter(models.Model):
    id_letter_mail = models.IntegerField()
    msg_time_send = models.CharField(max_length=255)
    msg_time_got = models.CharField(max_length=255)
    return_email_path = models.CharField(max_length=255)
    theme = models.CharField(max_length=255)
    to = models.CharField(max_length=255)
    sender = models.CharField(max_length=255)
    description = models.TextField()
    attachments = ArrayField(FileField(), null=True)

    class Meta:
        db_table = 'MailLetter'
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'

class UsersMails(models.Model):
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    str_system = models.CharField(max_length=255)

    def __str__(self):
        return f"Email: {self.email}\nMail: {self.str_system}"

    class Meta:
        db_table = 'UsersMails'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
