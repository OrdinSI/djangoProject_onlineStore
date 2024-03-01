from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.models import Blog


class BlogListView(ListView):
    model = Blog


class BlogDetailView(DetailView):
    model = Blog



class BlogCreateView(CreateView):
    model = Blog


class BlogUpdateView(UpdateView):
    model = Blog


class BlogDeleteView(DeleteView):
    model = Blog
