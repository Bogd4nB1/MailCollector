MailCollector
Это приложение собирает все ВХОДЯЩИЕ письма с вашего почтового ящика.
ВАЖНО! Для работы с приложением нжуно создать приложение в почте и разрешить проткол Imap.
Работает только с Yandex, Google, Mail.
Необходимо иметь установленный Python 3.10, PostgreSQL

1. mkdir MailCollector
2. cd MailCollector
3. git clone git@github.com:Bogd4nB1/MailCollector.git
4. python -m venv venv
5. venv\Scripts\activate
6. cd MailCollector
7. pip install -r requirements.txt
В settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'имя_базыданных',
        'USER': 'имя',
        'PASSWORD': 'пароль',
        'HOST': 'localhost',
        'PORT': '5432', //Если указывали другой порт при установке ставьте его
    }
}
8. python manage.py makemigrations appYandex
9. python manage.py migrate
10. python manage.py runserver

11. python manage.py createsuperuser
