from django.urls import path
from rest_framework.routers import DefaultRouter
from folders.views import (
    FolderViewSet, add_bookmark_to_folder,
    remove_bookmark_from_folder
)

router = DefaultRouter()
router.register(r'folders', FolderViewSet, basename='folder')

urlpatterns = [
    path('folders/add-bookmark/', add_bookmark_to_folder, name='add_bookmark_to_folder'),
    path('folders/remove-bookmark/', remove_bookmark_from_folder, name='remove_bookmark'),
] +  router.urls