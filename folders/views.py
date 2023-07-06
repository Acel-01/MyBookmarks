from rest_framework import viewsets
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.exceptions import NotFound
from rest_framework.throttling import UserRateThrottle
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
    throttle_classes = [UserRateThrottle]
    serializer_class = FolderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Folder.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = serializer.data
        data["message"] = f"Folder created successfully with name {data['name']}"
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data["message"] = f"Details of folder with uuid: {data['uuid']}"
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        data = serializer.data
        data["message"] = f"Folder with uuid: {data['uuid']} updated successfully"
        return Response(data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
            message = data[0]
            message["message"]=f'List of {request.user.email} folders gotten successfully.',
            return self.get_paginated_response(data)

        serializer = self.get_serializer(queryset, many=True)
        data = {
            "message": f'List of {request.user.email} folders gotten successfully.',
            "data_body_": serializer.data
        }
        return Response(data)

@api_view(['POST'])
@throttle_classes([UserRateThrottle])
def add_bookmark_to_folder(request):
    context = {'request': request}
    serializer = ValidateInputFolderSerializer(data=request.data, context=context)
    try:
        if serializer.is_valid():
            bookmark_id = request.data.get('bookmark')
            folder_name = request.data.get('name')

            bookmark = Bookmark.objects.filter(user=request.user, id=bookmark_id).first()
            if not bookmark:
                raise NotFound("Bookmark not found")

            folder = Folder.objects.filter(user=request.user, name=folder_name).first()
            if folder:
                if folder.bookmark.filter(id=bookmark.id):
                    pass
                else:
                    folder.bookmark.add(bookmark)
                serializer = FolderSerializer(folder, many=False)
                data = serializer.data
                data["message"] = f"Bookmark has been added to Folder with uuid: {folder.uuid}"
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                raise NotFound("Folder not found")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"message": e}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@throttle_classes([UserRateThrottle])
def remove_bookmark_from_folder(request):
    context = {'request': request}
    serializer = ValidateInputFolderSerializer(data=request.data, context=context)
    try:
        if serializer.is_valid():
            bookmark_id = request.data.get('bookmark')
            folder_name = request.data.get('name')

            bookmark = Bookmark.objects.filter(user=request.user, id=bookmark_id).first()
            if not bookmark:
                raise NotFound("Bookmark not found")

            folder = Folder.objects.filter(user=request.user, name=folder_name).first()
            if folder:
                folder.bookmark.remove(bookmark)
                return Response(data ={"message": f"Bookmark has been removed from Folder with uuid: {folder.uuid}"}, status=status.HTTP_200_OK)
            else:
                raise NotFound("Folder not found")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"message": e}, status=status.HTTP_400_BAD_REQUEST)
