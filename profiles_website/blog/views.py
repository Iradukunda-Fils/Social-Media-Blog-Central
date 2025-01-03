from django.db.models.query import QuerySet
from blog.models import Post
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import (ListView, DetailView, CreateView,UpdateView,DeleteView)
from django.urls import reverse_lazy

# Create your views here.

class PostListView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5
    login_url = 'login'
    
class UserPostListView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5
    login_url = 'login'
    
    def get_queryset(self) -> QuerySet[any]:
        user = get_object_or_404(User, username = self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
    
class PostDitailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    login_url = 'login'

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content']
    template_name = 'blog/post_creation.html'
    login_url = 'login'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title','content']
    template_name = 'blog/post_update.html'
    
    def get_success_url(self):
        # Redirect to the post detail page after successful update
        return reverse_lazy('post-detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user ==  post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Post
    fields = ['title','content']
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('blog-home')  
    
    
    def test_func(self):
        post = self.get_object()
        if self.request.user ==  post.author:
            return True
        return False


@login_required(login_url='login')
def about(request):
    return render(request,'blog/about.html')


