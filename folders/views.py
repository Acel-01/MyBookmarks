from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from folders.models import Folder
from bookmarks.models import Bookmark
from folders.serializers import (
    FolderSerializer, 
    ValidateInputFolderSerializer
)

# Create your views here.
class FolderViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing the 
    folders associated with the user.
    """
    serializer_class = FolderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Folder.objects.filter(user=user)
    

@api_view(['POST'])
def add_bookmark_to_folder(request):
    context = {'request':request}
    serializer = ValidateInputFolderSerializer(data=request.data, context=context)
    try:
        if serializer.is_valid():
            bookmark_id = request.data.get('bookmark')
            folder_name = request.data.get('name')

            bookmark = Bookmark.objects.filter(user=request.user,id=bookmark_id).first()
            if not bookmark:
                return Response({"detail": "Bookmark not found."}, status=status.HTTP_404_NOT_FOUND)
                
            folder = Folder.objects.filter(user=request.user,name=folder_name).first()
            if folder:
                if folder.bookmark.filter(id=bookmark.id):
                    pass
                else:
                    folder.bookmark.add(bookmark)
                serializer = FolderSerializer(folder, many=False)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Folder not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"detail": e}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def remove_bookmark_from_folder(request):
    context = {'request':request}
    serializer = ValidateInputFolderSerializer(data=request.data, context=context)
    try:
        if serializer.is_valid():
            bookmark_id = request.data.get('bookmark')
            folder_name = request.data.get('name')

            bookmark = Bookmark.objects.filter(user=request.user,id=bookmark_id).first()
            if not bookmark:
                return Response({"detail": "Bookmark not found."}, status=status.HTTP_404_NOT_FOUND)
                
            folder = Folder.objects.filter(user=request.user,name=folder_name).first()
            if folder:
                folder.bookmark.remove(bookmark)
                return Response(status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Folder not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"detail": e}, status=status.HTTP_400_BAD_REQUEST)