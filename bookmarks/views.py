from rest_framework import viewsets
from rest_framework.throttling import UserRateThrottle
from rest_framework.response import Response
from rest_framework import status
from django.db.models.query import prefetch_related_objects
from my_bookmarks.settings import get_throttle_time
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
        headers['X-Rate-Limit-Limit'] = get_throttle_time()
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, headers={'X-Rate-Limit-Limit': get_throttle_time()})
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, headers={'X-Rate-Limit-Limit': get_throttle_time()})
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        queryset = self.filter_queryset(self.get_queryset())
        if queryset._prefetch_related_lookups:
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance,
            # and then re-prefetch related objects
            instance._prefetched_objects_cache = {}
            prefetch_related_objects([instance], *queryset._prefetch_related_lookups)

        return Response(serializer.data, headers={'X-Rate-Limit-Limit': get_throttle_time()})
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT, headers={'X-Rate-Limit-Limit': get_throttle_time()})