import os
import re
import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Post(models.Model):
    message = models.TextField()
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts"
    )

    def __str__(self) -> str:
        return self.message

    def hashtags(self) -> list[str]:
        """
        finds all hashtags and parses them,
        returns list with all hashtags
        """
        pattern = re.compile(r"#\w+")

        matches = pattern.findall(self.message)
        hashtags = [match[1:] for match in matches]
        return hashtags

    def message_short(self) -> str:
        return self.message[:15]


def post_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.id)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/posts/", filename)


class PostImage(models.Model):
    image = models.ImageField(null=True, upload_to=post_image_file_path)
    title = models.CharField(max_length=55, unique=True)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="Images"
    )

    def __str__(self) -> str:
        return f"{self.post} - {self.image.url}"
