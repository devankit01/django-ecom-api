from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import json

class OTP_MAIL:
    def sendMailTemplate(context):  
        f = open('modules/otp_mail.json')
        data = json.load(f)
        f.close()
        data['otp'] = context['otp']
        if 'subject' in context.keys():
            data['subject'] = context['subject']
        if 'otp_body' in context.keys():
            data['otp_body'] = context['otp_body']
        if 'otp_text' in context.keys():
            data['otp_text'] = context['otp_text']
        try:
            message = render_to_string('otp_mail.html', data)
            to_email = context['email']
            print(to_email)
            msg = EmailMultiAlternatives(
                data['subject'], message, 'youremail', [to_email])
            msg.attach_alternative(message, "text/html")
            msg.send()
            return True
        except Exception as error:
            print(error,'-0-0')
            return False, error