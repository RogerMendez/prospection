from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail

import random

def create_code_activation():
    li = ['Q','W','E','R','T','Y','U','I','O','P','A','S','D','F','G','H','J','K','L','Z','X','C','V','B','N','M','1','2','3','4','5','6','7','8','9','0']
    #51 elementos
    code = random.choice(li)
    for i in range(50):
         code += random.choice(li)
    return code


def send_email(email, html):
    subject = 'Codigo De Activacion'
    text_content = 'Mensaje...nLinea 2nLinea3'
    html_content = html
    from_email = '"Prospection" <sieboliva@gmail.com>'
    to = email
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    #send_mail('Subject here', html, 'from@example.com', [], fail_silently=False)