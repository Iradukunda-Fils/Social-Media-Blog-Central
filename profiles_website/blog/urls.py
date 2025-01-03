from django.urls import path
from .views import  (PostListView, 
                     PostDitailView,
                     PostCreateView,
                     PostUpdateView,
                     PostDeleteView,
                     UserPostListView,
                     about,
                     )

urlpatterns = [
    path('',PostListView.as_view(),name='blog-home'),
    path('user/<str:username>/',UserPostListView.as_view(),name='user-posts'),
    path('post/<int:pk>/',PostDitailView.as_view(),name='post-detail'),
    path('post/new/',PostCreateView.as_view(),name='post-create'),
    path('post/<int:pk>/update/',PostUpdateView.as_view(),name='post-update'),
    path('post/<int:pk>/delete/',PostDeleteView.as_view(),name='post-delete'),
    path('about/',about,name='blog-about'),
]