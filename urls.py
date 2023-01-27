from django.urls import path

from . import views


app_name = 'blog'
urlpatterns = [
    path('', views.BlogView.as_view(), name="blog"),
    path('post/', views.PostView.as_view(), name="post"),
    path('blog-list/', views.BlogListView.as_view(), name="blog_list"),
    path('blog-mylist/', views.BlogMyListView.as_view(), name="blog_mylist"),
    path('released-blog-list/', views.ReleasedBlogListView.as_view(), name="released_blog_list"),
    path('blog-detail/<int:pk>/', views.BlogDetailView.as_view(), name="blog_detail"),
    path('released-blog-detail/<int:pk>/', views.ReleasedBlogDetailView.as_view(), name="released_blog_detail"),
    path('blog-create/', views.BlogCreateView.as_view(), name="blog_create"),
    path('blog-update/<int:pk>/', views.BlogUpdateView.as_view(), name="blog_update"),
    path('blog-delete/<int:pk>/', views.BlogDeleteView.as_view(), name="blog_delete"),
    path('profile/', views.ProfileView.as_view(), name="profile"),
]