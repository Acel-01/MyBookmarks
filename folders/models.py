import uuid
from django.db import models
from users.models import User
from bookmarks.models import Bookmark

# Create your models here.
class Folder(models.Model):
    uuid = models.UUIDField(
        primary_key = True, 
        default = uuid.uuid4,
        editable = False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(blank=False, null=False, max_length=150)
    bookmark = models.ManyToManyField(Bookmark)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date_created"]
        verbose_name_plural = "Folders"

    def __str__(self):
        return f"{self.name} - {self.bookmark.all().count()}"