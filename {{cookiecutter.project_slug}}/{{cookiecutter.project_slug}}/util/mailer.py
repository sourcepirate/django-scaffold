from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMessage
from django.conf import settings


def send_email(
    template_name, context, from_address=None, to_address=None, subject=None
):
    html_message = render_to_string(template_name, context)
    msg = EmailMessage(
        subject=subject,
        body=html_message,
        from_email=from_address,
        to=to_address,
    )
    msg.content_subtype = "html"  # Main content is now text/html
    return msg.send()


def is_public_email(email):
    """is public email id"""
    return any(map(lambda x: x in email, settings.PUBLIC_DOMAIN_TYPE))
