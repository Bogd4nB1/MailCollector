from email.header import decode_header
from bs4 import BeautifulSoup # type: ignore
from django.conf import settings
from channels.generic.websocket import WebsocketConsumer # type: ignore
from appYandex.models import Letter, UsersMails

import imaplib
import email
import os
import re
import datetime
import json


# Http protocol
def get_all(msg, email_id, str_system):
    date_tuple = email.utils.parsedate_tz(msg['Date'])

    if date_tuple:
        local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
        local_date = local_date.strftime('%a, %d %b %Y %H:%M:%S')
    else:
        local_date = None

    id_letter = int(email_id.decode('utf-8'))
    msg_time_send = msg['Date']
    msg_time_got = local_date

    try:
        return_email_path = decode_header(msg['From'])[0][0]
        if type(return_email_path) == bytes:
            return_email_path = return_email_path.decode()
        else:
            return_email_path = return_email_path
    except:
        return_email_path = msg['Return-path']

    try:
        theme = decode_header(msg["Subject"])[0][0].decode()
        if type(theme) == bytes:
            theme = theme.decode()
        else:
            theme = theme
    except:
        theme = msg["Subject"]

    try:
        to = decode_header(msg["To"])[0][0].decode()
        if type(to) == bytes:
            to = to.decode()
        else:
            to = to
    except:
        to = msg["To"]

    try:
        sender = decode_header(msg["From"])[0][0].decode()
        if type(sender) == bytes:
            sender = sender.decode()
        else:
            sender = sender
    except:
        sender = msg["From"]

    output_path = os.path.join(settings.BASE_DIR, 'output')
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    attachment = []

    for part in msg.walk():
        content_type = part.get_content_type()
        clear_content_type = content_type.split('/')[0]

        if part.get_content_disposition() == 'attachment':
            filename = part.get_filename()
            if filename:
                filename_bytes = decode_header(filename)[0][0]
                filename = filename_bytes.decode() if isinstance(filename_bytes, bytes) else filename
        
        if clear_content_type == 'image' or clear_content_type == 'video' or clear_content_type == 'audio' or clear_content_type == 'application':
            if filename:
                with open(os.path.join(output_path, filename), 'wb') as file:
                    file.write(part.get_payload(decode=True))

                attachment.append(filename)
                print(f"Файл: {filename} сохранен")
                
        if content_type == 'text/plain':
            body = part.get_payload(decode=True).decode()

        if content_type == 'text/html':
            body = part.get_payload(decode=True).decode()
            soup = BeautifulSoup(body, "html.parser")
            tags = ['div', 'p', 'h1', 'h2', 'span']
            found_tags = soup.find_all(tags)
            some_text = ''
            for div in found_tags:
                text = re.sub(r'\s+', ' ', div.get_text())
                some_text += text + '\n'
            body = some_text
    
    Letter.objects.create(
        id_letter_mail = id_letter,
        msg_time_send = msg_time_send,
        msg_time_got = msg_time_got,
        return_email_path = return_email_path,
        theme = theme,
        to = to,
        sender = sender,
        description = body,
        attachments = attachment
    )

    letter = Letter.objects.last()
    return letter

def choice_system(ch):
    if ch == 'yandex':
        mail_server = 'imap.yandex.ru'
        return mail_server
    
    if ch == 'gmail':
        mail_server = 'imap.gmail.com'
        return mail_server

    if ch == 'mail':
        mail_server = 'imap.mail.ru'
        return mail_server


# Websocket protocol
class WSMailConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        
        user = UsersMails.objects.first()
        mail = imaplib.IMAP4_SSL(choice_system(user.str_system))
        mail.login(user.email, user.password)
        quantity_mails = mail.select('inbox')

        res, msg = mail.uid('search', None, "ALL") # Выполняет поиск и возвращает UID писем.
        email_uid = msg[0].split()
        len_email_uid = len(email_uid)
        c = 0
        
        Letter.objects.all().delete()
            
        for email_id in email_uid:
            result, msg = mail.uid('fetch', email_id, '(RFC822)')
            msg = email.message_from_bytes(msg[0][1])

            # Функции для получения содержимого письма
            lt = get_all(msg, email_id, user.str_system)
            c = c + 1
            self.send(json.dumps({
                'message': f'Письмо {c} получено',
                'id_letter_mail': lt.id_letter_mail,
                'msg_time_send': lt.msg_time_send,
                'msg_time_got': lt.msg_time_got,
                'return_email_path': lt.return_email_path,
                'theme': lt.theme,
                'to': lt.to,
                'sender': lt.sender,
                'description': lt.description,
                'attachments': lt.attachments,
                'number_letter': c,
                'len_uid': len_email_uid
            }))

        if c == len_email_uid:
            print('Все письма получены')
        else:
            print('Не все письма получены')

        mail.logout()

        self.close()
    

