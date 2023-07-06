from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from folders.models import Folder
from bookmarks.models import Bookmark
from users.serializers import UserSerializer

class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ['uuid', 'user', 'title', 'link', 'date_created']
        read_only_fields = ('user',)


class FolderSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    bookmark = BookmarkSerializer(many=True, read_only=True)
    class Meta:
        model = Folder
        fields = ['uuid', 'user', 'name', 'bookmark', 'date_created']
        read_only_fields = ('user',)

class ValidateInputFolderSerializer(serializers.Serializer):
    # user = UserSerializer(many=False, read_only=True)
    bookmark = serializers.UUIDField(format='hex_verbose')
    folder = serializers.UUIDField(format='hex_verbose')

    def validate_bookmark(self, value):
        request = self.context["request"]

        bookmark = Bookmark.objects.filter(user=request.user, uuid=value)
        if bookmark:
            return bookmark[0]
        else:
            raise ValidationError("Bookmark not found")

    def validate_folder(self, value):
        request = self.context["request"]

        folder = Folder.objects.filter(user=request.user, uuid=value)
        if folder:
            return folder[0]
        else:
            raise ValidationError("Folder not found")

    # class Meta:
    #     model = Folder
    #     fields = ['uuid', 'user', 'name', 'bookmark', 'date_created']
    #     read_only_fields = ('user',)