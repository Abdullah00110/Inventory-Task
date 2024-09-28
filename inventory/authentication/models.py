from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class MyUserManager(BaseUserManager):
    """
    Custom manager for MyUser to handle user creation and management.
    """
    def create_user(self, username, email, tc, password=None, password2=None):
        """
        Creates and saves a User with the given username, email, and password.
        """
        if not username:
            raise ValueError("Users must have a username")
        if not email:
            raise ValueError("Users must have an email address")
        # if password is None or len(password) < 8:  # Password validation example
        #     raise ValueError("Password must be at least 8 characters long")
        # if password != password2:
        #     raise ValueError("Passwords must match")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            tc=tc,
            # password = password,
            # password2 = password2,
        )

        user.set_password(password)  # Hash the password before saving
        user.save(using=self._db)  # Save the user to the database
        return user

    def create_superuser(self, username, email, tc, password=None):
        """
        Creates and saves a superuser with the given username, email, and password.
        """
        user = self.create_user(
            username=username,
            email=email,
            tc=tc,
            password=password,
            password2=password,  # For superuser creation, assume passwords match
        )
        user.is_admin = True  # Set admin status to True
        user.is_active = True  # Ensure the superuser is active
        user.save(using=self._db)  # Save the superuser to the database
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=255, unique=True)  # Unique username field
    tc = models.BooleanField()  # Terms and conditions acceptance
    is_active = models.BooleanField(default=True)  # User is active by default
    is_admin = models.BooleanField(default=False)  # User is admin by default
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when user is created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when user is updated

    objects = MyUserManager()  # Custom user manager

    USERNAME_FIELD = 'username'  # Set the login field as 'username'
    REQUIRED_FIELDS = ['email', 'tc']  # Email and tc are required for user creation

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        """
        Return True if the user has the specified permission.
        """
        return True

    def has_module_perms(self, app_label):
        """
        Return True if the user has permissions to view the app `app_label`.
        """
        return True

    @property
    def is_staff(self):
        """
        Is the user a member of staff? Superuser/admin users are considered staff.
        """
        return self.is_admin

