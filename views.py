import logging
from platform import release
from urllib import request

from django.urls import reverse_lazy
from django.shortcuts import render
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.db.models import Q

from .forms import PostForm, BlogCreateForm
from .models import Blog

from accounts.models import CustomUser


logger = logging.getLogger(__name__)

# Create your views here.
class BlogView(generic.TemplateView):
    template_name = "blog_index.html"


class PostView(generic.FormView):
    template_name = 'post.html'
    form_class = PostForm
    success_url = reverse_lazy('blog:post')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました。')
        logger.info('Post sent by {}'.format(form.cleaned_data['post_name']))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'メッセージの送信に失敗しました。')
        return super().form_invalid(form)

    
class BlogListView(LoginRequiredMixin, generic.ListView):
    model = Blog
    template_name = 'blog_list.html'
    paginate_by = 3

    def get_queryset(self):
        blogs = Blog.objects.filter(user=self.request.user).order_by('-created_at')
        return blogs


class BlogMyListView(LoginRequiredMixin, generic.ListView):
    model = Blog
    template_name = 'blog_mylist.html'
    paginate_by = 10

    # def get_queryset(self):
    #     blogs = Blog.objects.filter(user=self.request.user).order_by('-created_at')
    #     return blogs

    def get_queryset(self):
        queryset = Blog.objects.filter(user=self.request.user).order_by('-created_at')
        query = self.request.GET.get('query')

        if query:
            # queryset = queryset.filter(Q(title__icontains=query))
            # queryset = queryset.filter(Q(title__icontains=query) | Q(content__icontains=query))
            queryset = queryset.filter(Q(user__username=query) | Q(title__icontains=query) | Q(content__icontains=query))
        
        return queryset


class ReleasedBlogListView(LoginRequiredMixin, generic.ListView):
    model = Blog
    template_name = 'released_blog_list.html'
    paginate_by = 10

    # def get_queryset(self):
    #     blogs = Blog.objects.order_by('-created_at')
    #     return blogs

    # def get_form_queryset(self):
    #     if "order_by" in self.request.GET:
    #         queryset = Blog.objects.order_by(self.request.GET['order_by'])

    #     return queryset

    def get_queryset(self):
        queryset = Blog.objects.filter(release_flag=1).order_by('-created_at')
        query = self.request.GET.get('query')

        if query:
            # queryset = queryset.filter(Q(title__icontains=query))
            # queryset = queryset.filter(Q(title__icontains=query) | Q(content__icontains=query))
            queryset = queryset.filter(Q(user__username=query) | Q(title__icontains=query) | Q(content__icontains=query))
            
        return queryset


class BlogDetailView(LoginRequiredMixin, generic.DetailView):
    model = Blog
    template_name = 'blog_detail.html'


class ReleasedBlogDetailView(LoginRequiredMixin, generic.DetailView):
    model = Blog
    template_name = 'released_blog_detail.html'


class BlogCreateView(LoginRequiredMixin, generic.CreateView):
    model = Blog
    template_name = 'blog_create.html'
    form_class = BlogCreateForm
    success_url = reverse_lazy('blog:blog_mylist')

    def form_valid(self, form):
        diary = form.save(commit=False)
        diary.user = self.request.user
        diary.save()
        messages.success(self.request, 'ブログを作成しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "ブログの作成に失敗しました。")
        return super().form_invalid(form)


class BlogUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Blog
    template_name = 'blog_update.html'
    form_class = BlogCreateForm

    def get_success_url(self):
        return reverse_lazy('blog:blog_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        messages.success(self.request, 'ブログを更新しました。')
        # update = Blog.objects.filter(pk=object.pk).get(updated_flag=1)
        update = form.save(commit=False)
        update.updated_flag = 2
        update.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "ブログの更新に失敗しました。")
        return super().form_invalid(form)


class BlogDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Blog
    template_name = 'blog_delete.html'
    success_url = reverse_lazy('blog:blog_mylist')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "ブログを削除しました。")
        return super().delete(request, *args, **kwargs)
    

class ProfileView(LoginRequiredMixin, generic.ListView):
    # model = CustomUser
    model = Blog
    template_name = 'profile.html'

    def get_queryset(self):
        # customusers = CustomUser.objects.filter(username=self.request.user)
        customusers = Blog.objects.filter(user=self.request.user)
        return customusers
