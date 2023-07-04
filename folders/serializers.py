from rest_framework import serializers
from folders.models import Folder
from bookmarks.models import Bookmark
from users.serializers import UserSerializer

class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ['id', 'user', 'text', 'date_created']
        read_only_fields = ('user',)


class FolderSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    bookmark = BookmarkSerializer(many=True, read_only=True)
    class Meta:
        model = Folder
        fields = ['id', 'user', 'name', 'bookmark', 'date_created']
        read_only_fields = ('user',)

class ValidateInputFolderSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    bookmark = serializers.UUIDField(format='hex_verbose')
    class Meta:
        model = Folder
        fields = ['id', 'user', 'name', 'bookmark', 'date_created']
        read_only_fields = ('user',)