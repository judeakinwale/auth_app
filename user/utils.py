from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template
from user.serializers import UserSerializer
from company.serializers import EmployeeResponseSerializer


def send_account_creation_email(request, reciepients: list, context: dict = {}) -> bool:
  """
  reciepients is an array of reciepient email addresses
  context should contain:
    'company': company,
    'user': user,
    'url': url,
  """
  try:
    subject = "Account Created"
    sender_email = settings.EMAIL_HOST_USER

    message = get_template('email/account_creation.html').render(context)

    msg = EmailMessage(
      subject,
      message,
      sender_email,
      reciepients,
    )
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()

    print(f"\nMail successfully sent: {msg}")
    return True
  except Exception as e:
    print(f"There was an exception sending mail: {e}")
    return False