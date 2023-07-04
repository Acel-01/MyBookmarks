from django.urls import path
from bookmarks.views import (
    BookmarkCreate, BookmarkList, BookmarkRetrieve, 
    BookmarkUpdate, BookmarkDelete
)

urlpatterns = [
    path('create/', BookmarkCreate.as_view(), name='bookmark_create'),
    path('list/', BookmarkList.as_view(), name='bookmark_list'),
    path('retrieve/<str:pk>/', BookmarkRetrieve.as_view(), name='bookmark_retrieve'),
    path('update/<str:pk>/', BookmarkUpdate.as_view(), name='bookmark_update'),
    path('delete/<str:pk>/', BookmarkDelete.as_view(), name='bookmark_delete'),
]