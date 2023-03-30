from django.urls import path

from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('post/', CreatePostView.as_view(), name='add_post'),
    path('post/<int:pk>/', PostView.as_view(), name='view_post'),
    path('post/<int:pk>/update/', UpdatePostView.as_view(), name='update_post'),
    path('post/<int:pk>/delete/', DeletePostView.as_view(), name='delete_post'),
    path('post/<int:pk>/reply', ShowReplyView.as_view(), name='show_reply'),
    path('reply/', AuthorReplyView.as_view(), name='author_reply'),
    path('reply/<int:pk>/delete/', DeleteReplyView.as_view(), name='delete_reply'),
    path('reply/<int:pk>/confirm/', UpdateReplyView.as_view(), name='confirm_reply'),
]
