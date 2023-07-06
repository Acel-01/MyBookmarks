from rest_framework import serializers
from users.serializers import UserSerializer
from bookmarks.models import Bookmark


class BookmarkSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Bookmark
        fields = ['uuid', 'user', 'title', 'link', 'date_created']
        read_only_fields = ('user',)
        extra_kwargs = {"link": {"error_messages": {"invalid": "Enter a valid URL. e.g https://google.com"}}}