from rest_framework import generics
from bookmarks.models import Bookmark
from bookmarks.serializers import BookmarkSerializer

# Create your views here.
class BookmarkList(generics.ListAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer

    def get_queryset(self):
        user = self.request.user
        return Bookmark.objects.filter(user=user)

class BookmarkCreate(generics.CreateAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BookmarkRetrieve(generics.RetrieveAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer

    def get_queryset(self):
        user = self.request.user
        return Bookmark.objects.filter(user=user)
    
class BookmarkUpdate(generics.UpdateAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer

    def get_queryset(self):
        user = self.request.user
        return Bookmark.objects.filter(user=user)
    
class BookmarkDelete(generics.DestroyAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer

    def get_queryset(self):
        user = self.request.user
        return Bookmark.objects.filter(user=user)