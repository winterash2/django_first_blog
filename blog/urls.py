from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # ''는 아무것도 없는 것을 의미함 즉 localhost:8000 여기를 의미함
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    #localhost:8000/post/new
    path("post/new", views.post_new, name='post_new'),
    #localhost:8000/5/edit
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    #localhost:8000/5/remove
    path('post/<int:pk>/remove/', views.post_remove, name='post_remove'),
    #localhost:8000/5/comment
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    #comment 승인, 삭제
    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
]