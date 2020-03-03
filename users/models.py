from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator


class UserManager(BaseUserManager):

  def _create_user(self, email, password):
    if not email:
        raise ValueError('Users must have an email address')
    now = timezone.now()
    email = self.normalize_email(email)
    user = self.model(
        email=email,
        last_login=now,
        date_joined=now, 
    )
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, email, password):
    return self._create_user(email, password, False, False)

  def create_superuser(self, email, password):
    user=self._create_user(email, password, True, True)
    user.save(using=self._db)
    return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254, null=True, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?9?\d{10}$', message="Phone number must be entered in the format: '+9999999999'. Up to 10 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=13, blank=False, unique=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)
