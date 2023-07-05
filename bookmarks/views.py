from rest_framework import viewsets
from bookmarks.models import Bookmark
from bookmarks.serializers import BookmarkSerializer

# Create your views here.
class BookmarkViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing the 
    bookmarks associated with the user.
    """
    serializer_class = BookmarkSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Bookmark.objects.filter(user=user)
