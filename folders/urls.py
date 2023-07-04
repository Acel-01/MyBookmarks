from django.urls import path
from folders.views import (
    FolderCreate, FolderList, FolderRetrieve, 
    FolderUpdate, FolderDelete, add_bookmark_to_folder,
    remove_bookmark_from_folder
)

urlpatterns = [
    path('create/', FolderCreate.as_view(), name='folder_create'),
    path('list/', FolderList.as_view(), name='folder_list'),
    path('retrieve/<str:pk>/', FolderRetrieve.as_view(), name='folder_retrieve'),
    path('update/<str:pk>/', FolderUpdate.as_view(), name='folder_update'),
    path('delete/<str:pk>/', FolderDelete.as_view(), name='folder_delete'),
    path('add_bookmark/', add_bookmark_to_folder, name='add_bookmark_to_folder'),
    path('remove_bookmark/', remove_bookmark_from_folder, name='remove_bookmark'),
]