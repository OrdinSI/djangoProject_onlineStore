
from blog.apps import BlogConfig
from django.urls import path
from blog.views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView, publish


app_name = BlogConfig.name

urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path("blog_create/", BlogCreateView.as_view(), name='blog_create'),
    path("blog_detail/<int:pk>/", BlogDetailView.as_view(), name='blog_detail'),
    path("blog_delete/<int:pk>/", BlogDeleteView.as_view(), name='blog_delete'),
    path("blog_update/<int:pk>/", BlogUpdateView.as_view(), name='blog_update'),
    path("publish/<int:pk>/", publish, name='publish'),
]
