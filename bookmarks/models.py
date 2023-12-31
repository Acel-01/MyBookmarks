import uuid
from django.db import models
from users.models import User


# Create your models here.
class Bookmark(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(blank=False, null=False, max_length=2000)
    link = models.URLField(blank=False, error_messages={"invalid": "Enter a valid URL. e.g https://google.com"},
                           null=False, max_length=2000)

    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date_created"]
        verbose_name_plural = "Bookmarks"

    def __str__(self):
        return f"{self.title}"
