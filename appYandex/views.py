from django.shortcuts import render, HttpResponseRedirect
from .utils import choice_system
from appYandex.models import UsersMails, Letter
from django.http import HttpResponse
from django.conf import settings
import imaplib
import os
import shutil


output_path = os.path.join(settings.BASE_DIR, 'output')

def index(request):
    return render(request, 'index.html')

def mails(request):
    return render(request, 'mails.html')

def register_or_login(request, output_path=output_path):
    error = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        str_system = request.POST.get('str_system')
        try:
            # Делаем проверку есть ли подключение или нет
            mail = imaplib.IMAP4_SSL(choice_system(str_system))
            mail.login(email, password)
            # Отключаем соединение
            mail.logout()
            UsersMails.objects.all().delete() # Так как система完全но одноразовая я всегда оставляю только одного юзера
            UsersMails.objects.create(email=email, password=password, str_system=str_system)
            if os.path.exists(output_path):
                shutil.rmtree(output_path)
                print('Папка удалена')
            
            print('Пользователь зарегистрирован')
            return HttpResponseRedirect('/mails/')
        except:
            error = 'Неверный логин или пароль'
    return render(request, 'index.html', {"error": error})

def download_file(request):
    if request.method == 'POST':
        string = request.POST.get('attachments')
        attach = Letter.objects.get(id_letter_mail=string).attachments
        if type(attach) is not list:
            file_path = os.path.join(settings.BASE_DIR, 'output', attach[0])
            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    resp = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                    resp['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                    return resp
        else:
            for file in attach:
                file_path = os.path.join(settings.BASE_DIR, 'output', file)
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as fh:
                        resp = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                        resp['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                        return resp
            # если ни один файл не найден, возвращаем пустую страницу
            return HttpResponse("No files found")
    return HttpResponse("Download file page")
    
