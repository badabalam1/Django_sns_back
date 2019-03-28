from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [
    path('user/<int:limit_id>/<int:user_id>/',
         view=MyPost.as_view(), name='my_post'),
    path('list/<int:limit_id>/', view=Post_List.as_view(), name='post_list'),
    path("write/", view=Post.as_view(), name='Post'),
    path("<int:post_id>/", view=Post.as_view(), name='Post_REST'),
    path("comment/<int:post_id>/",
         view=Comment.as_view(), name='Comment'),
    path("comment/<int:post_id>/<int:comment_id>/",
         view=Comment_REST.as_view(), name='Comment_REST'),
] + static(settings.POST_IMAGE_URL, document_root=settings.POST_IMAGE_ROOT)
