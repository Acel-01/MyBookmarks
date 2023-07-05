from rest_framework import serializers
from users.serializers import UserSerializer
from bookmarks.models import Bookmark

class BookmarkSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Bookmark
        fields = ['id', 'user', 'text', 'date_created']
        read_only_fields = ('user',)