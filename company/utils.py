from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


def get_tokens_for_employee(employee):
  user = employee.user
  refresh = RefreshToken.for_user(user)

  return {
    'refresh': str(refresh),
    'access': str(refresh.access_token),
  }


class EmployeeTokenObtainPairSerializer(TokenObtainPairSerializer):
  self.username_field = 'employee_id'
    
  def validate(self, attrs):
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