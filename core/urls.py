from django.urls import path
from . import views
urlpatterns = [
   path('posts/',views.PostListCreateView.as_view(),name='posts'),
   path('posts/tag/<slug:tag_slug>/',views.PostListCreateView.as_view(),name='posts_list_by_tag'),
   path('post/<int:year>/<int:month>/<int:day>/<slug:slug_post>/',views.PostUpdateDeleteView.as_view(),name='post_detail'),
   path('most_commented_post/',views.MostCommentedPost.as_view(),name='most_commented_post'),
   path('post/share/<uuid:post_id>/',views.PostShareView.as_view(),name='post_share'),
   path('<uuid:id>/comments/',views.CommentListView.as_view(),name='comment_list'),
   path('<uuid:id>/comment/add/',views.CommentCreateView.as_view(),name='comment_create'),
   path('comment/<uuid:comment_id>/update/',views.CommentUpdateView.as_view(),name='comment_Update'),

  
]
