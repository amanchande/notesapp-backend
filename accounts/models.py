from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from .validators import avatar_validator
from globals.global_config import GENDER
from globals.models import Timestamp

USER_STATUS = (
    ('active', 'active'),
    ('inactive', 'inactive'),
)

# Create your models here.
class UserManager(BaseUserManager):
    """
    Override the default methods create_user, create_superuser
    """

    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, username, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            username,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            username,
            password=password,
        )
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user

        
class User(PermissionsMixin, AbstractBaseUser):
    """
    Custom user model
    """

    # Custom fields
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    signup_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    # Permission fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # admin user; non super-user
    is_admin = models.BooleanField(default=False) # superuser
    is_server_admin = models.BooleanField(default=False) #access for server admin panel
    status = models.CharField(max_length=50, default="active", choices=USER_STATUS)

    # notice the absence of a "Password field", that's built in.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',] # Email & Password are required by default.

    objects = UserManager()

    # Methods inherited from AbstractBaseUser
    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self): 
        # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def if_staff(self):
        "Is the user a member of staff?"
        return self.is_staff

    @property
    def if_admin(self):
        "Is the user a admin member?"
        return self.is_admin

    @property
    def if_active(self):
        "Is the user active?"
        return self.is_active

    @property
    def if_server_admin(self):
        return self.is_server_admin

class Profile(Timestamp):
    """
    User Profile
    Extends Timestamp (Abstract Class) 
    pk: UUID
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    dob = models.DateTimeField(blank=True, null=True)
    avatar = models.ImageField(upload_to='profiles/', blank=True, null=True, validators=[avatar_validator])
    gender = models.CharField(max_length=25, blank=True, null=True, choices=GENDER)
    country = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profiles"

    def __str__(self):
        return self.user.email

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
    