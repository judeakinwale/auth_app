from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


def send_simple_email(request, template_path: str, reciepients: list, subject: str = "Email", context: dict = {}) -> bool:
  try:
    # subject = subject
    sender_email = settings.EMAIL_HOST_USER
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
    print(f"There was an exception sending mail: {e}")
    return False


def send_company_link(request, email: str) -> str:
  user = request.user
  print(user)
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
  except Exception as e:
    print(f'An exception occurred while sending the company link: {e}')
    
  return url


def get_tokens_for_employee(employee):
  user = employee.user
  refresh = RefreshToken.for_user(user)

  return {
    'refresh': str(refresh),
    'access': str(refresh.access_token),
  }


class EmployeeTokenObtainPairSerializer(TokenObtainPairSerializer):
  
  def validate(self, attrs):
    self.username_field = 'employee_id'
    
    authenticate_kwargs = {
      self.username_field: attrs[self.username_field],
      "password": attrs["password"],
    }
    super().validate(attrs)
  
  @classmethod
  def get_token(cls, user):
      # token = super().get_token(user)

      # Add custom claims
      token['name'] = user.name
      # ...

      return token


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