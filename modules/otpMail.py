from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


class OTP_MAIL:
    def sendMailTemplate(context,otp):
        try:
            message = render_to_string('otp_mail.html', {
                'user': context,
                'otp':otp,
            })
            to_email = context['email']
            msg = EmailMultiAlternatives(
                context['subject'], message, 'youremail', [to_email])
            msg.attach_alternative(message, "text/html")
            msg.send()
            return True
        except Exception as error:
            return False, error