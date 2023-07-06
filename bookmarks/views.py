from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from bookmarks.models import Bookmark
from bookmarks.serializers import BookmarkSerializer


# Create your views here.
class BookmarkViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing the 
    bookmarks associated with the user.
    """
    throttle_classes = [UserRateThrottle]
    serializer_class = BookmarkSerializer
    lookup_field = "uuid"

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Bookmark.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = serializer.data
        data["message"] = f"Bookmark created successfully with title {data['title']}"
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data["message"] = f"Details of bookmark with uuid: {data['uuid']}"
        return Response(data)

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
        data["message"] = f"Bookmark with uuid: {data['uuid']} updated successfully"
        return Response(data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
            message = data[0]
            message["message"]=f'List of {request.user.email} bookmarks gotten successfully.',
            return self.get_paginated_response(data)

        serializer = self.get_serializer(queryset, many=True)
        data = {
            "message": f'List of {request.user.email} bookmarks gotten successfully.',
            "data_body_": serializer.data
        }
        return Response(data)