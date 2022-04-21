from django.contrib.auth.models import BaseUserManager

# Create your managers here.


class UserManager(BaseUserManager):
    """user manager for the custom user model"""

    def create_user(self, email, password, **kwargs):
        """create and save a new user"""
        if not email:
            raise ValueError('Users must have a valid email address')
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_staff(self, email, password, **kwargs):
        """create and save a new staff"""
        user = self.create_user(email, password, **kwargs)
        # user.role = "Admin"
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        """create and save a new superuser"""
        user = self.create_user(email, password, **kwargs)
        # user.role = "Admin"
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
