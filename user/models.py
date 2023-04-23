import os
import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models, transaction
from django.utils.text import slugify
from django.utils.translation import gettext as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


def profile_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.email)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/users/", filename)


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    bio = models.TextField(null=True, blank=True)
    following = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="user_followers",
    )
    followers = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="user_following",
    )
    image = models.ImageField(null=True, upload_to=profile_image_file_path)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        ordering = ["email"]

    def __str__(self) -> str:
        return self.email

    @property
    def followers_count(self) -> int:
        return self.followers.count()

    @transaction.atomic
    def follow_unfollow_user(self, user):
        """
        Unfollow the specified user.
        """
        print(self, user)
        if self != user:
            if self.is_following(user):
                self.following.remove(user)
                user.followers.remove(self)
            else:
                self.following.add(user)
                user.followers.add(self)

    def is_following(self, user):
        """
        Check if the user is following the specified user.
        """
        return self.following.filter(id=user.id).exists()
