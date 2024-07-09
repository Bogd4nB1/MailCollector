from django.contrib import admin
from appYandex.models import Letter, UsersMails


@admin.register(Letter)
class MailLetterAdmin(admin.ModelAdmin):
    list_display =['id_letter_mail','msg_time_send','msg_time_got','return_email_path','theme','to','sender','description','attachments']

@admin.register(UsersMails)
class UsersMailsAdmin(admin.ModelAdmin):
    list_display = ['email','password','str_system']