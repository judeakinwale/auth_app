from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.urls import reverse
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from company import models


def send_simple_email(request, template_path: str, reciepients: list, subject: str = "Email", context: dict = {}) -> bool:
  try:
    # subject = subject
    # sender_email = settings.EMAIL_HOST_USER
    sender_email = f"{settings.DEFAULT_FROM_NAME} <{settings.EMAIL_HOST_USER}>"
    # context = context # context dictionary - {}
    message = get_template(template_path).render(context) # path to the email template - 'email/results.html'
    # reciepients = reciepients # list of emails

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
    # print(f"There was an exception sending mail: {e}")
    raise Exception(f"{e}")
    return False


def send_company_link(request, email: str) -> str:
  user = request.user
  # print(user)
  try:
    company = user.employee.company
  except:
    company = user.company
  # url = request.get_absolute_url()
  url = request.build_absolute_uri(reverse(f'company:employee-list')) 
  url += f"create?company={company.id}"
  
  context = {
    'company': company,
    'user': user,
    'url': url,
  }
  try:
    email = send_simple_email(request, 'email/company_link.html', [email], "Company Link", context)
    print(f'Company link sent {email}')
    return url
  except Exception as e:
    # print(f'An exception occurred while sending the company link: {e}')
    raise Exception(f'An exception occurred while sending the company link: {e}')
    


# def send_employee_event_email(request, employee) -> str:
def send_employee_event_email(request, employee, event_ids: list) -> str:
  try:
    company = employee.company
    name = f"{employee.user.first_name}"
    email = employee.user.email
    events = models.Event.objects.filter(
      Q(id__in=event_ids) 
      # & Q(company=company) 
      & Q(employee=employee) 
      # & ~Q(status="Completed") | ~Q(status="Dropped")
    )
    print(f"event ids: {event_ids}")
    print(f"employee company: {company}")
    print(f"employee: {employee}")
    print(f"email events: {events}")
    # events = events.filter(employee=employee)
    
    context = {
      'company': company,
      'events': events,
      'employee': employee,
      'name': name,
      # 'url': url,
    }
    try:
      email = send_simple_email(request, 'email/employee_event_email.html', [email], "Shift Details", context)
      print(f'Employee event nofitication mail sent {email}')
    except Exception as e:
      print(f'An exception occurred while sending the company link: {e}')
      
    # return url
    
  except Exception as e:
    print(f'An exception occurred while getting employee details: {e}')


# def send_client_event_email(request, client) -> str:
def send_client_event_email(request, client, event_ids: list) -> str:
  try:
    user = client.name
    email = client.email
    company = client.company
    url = "https:// " # link to frontend schedule page for client
    events = models.Event.objects.filter(
      Q(id__in=event_ids) 
      # & Q(company=company) 
      & Q(client=client) 
      # & ~Q(status="Completed") | ~Q(status="Dropped")
    )
    # events = events.filter(client=client)
    
    
    context = {
      'company': company,
      'events': events,
      'client': client,
      'name': user,
      'url': url,
    }
    try:
      email = send_simple_email(request, 'client_event_email.html', [email], "Company Link", context)
      print(f'Client event schedule email sent {email}')
      return True
    except Exception as e:
      print(f'An exception occurred while sending the event schedule: {e}')
      return False
      
    # return url
        
  except Exception as e:
    print(f'An exception occurred while getting client details: {e}')


# def send_employee_event_email(request, employee, events) -> str:
def send_employee_schedule_publish_email(request, employee) -> str:
  try:
    company = employee.company
    name = f"{employee.user.first_name}"
    email = employee.user.email
    # events = models.Event.objects.filter(
    #   Q(company=company) & Q(employee=employee) 
    #   # & ~Q(status="Completed") | ~Q(status="Dropped")
    # )
    
    context = {
      'company': company,
      # 'events': events,
      'employee': employee,
      'name': name,
      # 'url': url,
    }
    try:
      email = send_simple_email(request, 'email/employee_schedule_publish_email.html', [email], "Monthly Schedule", context)
      print(f'Employee schedule publish mail sent {email}')
    except Exception as e:
      print(f'An exception occurred while sending the company link: {e}')
      
    # return url
        
  except Exception as e:
    print(f'An exception occurred while getting employee details: {e}')


# def get_tokens_for_employee(employee):
#   user = employee.user
#   refresh = RefreshToken.for_user(user)

#   return {
#     'refresh': str(refresh),
#     'access': str(refresh.access_token),
#   }


# class EmployeeTokenObtainPairSerializer(TokenObtainPairSerializer):
  
#   def validate(self, attrs):
#     self.username_field = 'employee_id'
    
#     authenticate_kwargs = {
#       self.username_field: attrs[self.username_field],
#       "password": attrs["password"],
#     }
#     super().validate(attrs)
  
#   @classmethod
#   def get_token(cls, user):
#       # token = super().get_token(user)

#       # Add custom claims
#       token['name'] = user.name
#       # ...

#       return token


# class EmployeeTokenObtainPairView(TokenObtainPairView):
#     serializer_class = EmployeeTokenObtainPairSerializer


# Template for modifying the token obtain pair serializer
  """
  class TokenObtainSerializer(serializers.Serializer):
    username_field = get_user_model().USERNAME_FIELD
    token_class = None

    default_error_messages = {
        "no_active_account": _("No active account found with the given credentials")
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields["password"] = PasswordField()

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "password": attrs["password"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )

        return {}

    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)


class TokenObtainPairSerializer(TokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
  """