from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy

from .models import *
from .forms import PostForm, ReplyForm


# def model_form_upload(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = PostForm()
#     return render(request, 'post.html', {'form': form})


def model_form_upload(request):
    if request.method == 'POST':
        if 'post' in request.POST:
            post_form = PostForm(request.POST, request.FILES)
            if post_form.is_valid():
                post_form.save()
                return redirect('home')
        elif 'reply' in request.POST:
            reply_form = ReplyForm(request.POST)
            if reply_form.is_valid():
                reply_form.save()
                return redirect('home')
    else:
        post_form = PostForm()
        return render(request, 'post.html', {'post_form': post_form})


class HomePageView(ListView):
    queryset = Post.objects.all()
    template_name = 'home.html'
    ordering = '-time_create_post'
    context_object_name = 'homepage'
    paginate_by = 10


class PostView(DetailView):
    queryset = Post.objects.all()
    template_name = 'post_view.html'
    context_object_name = 'postview'


class CreatePostView(PermissionRequiredMixin, CreateView):
    permission_required = ('posts.add_post',)
    model = Post
    form_class = PostForm
    template_name = 'post.html'
    success_url = reverse_lazy('home')


class UpdatePostView(PermissionRequiredMixin, UpdateView):
    permission_required = ('posts.change_post',)
    model = Post
    form_class = PostForm
    template_name = 'post_update.html'
    success_url = reverse_lazy('home')


class DeletePostView(PermissionRequiredMixin, DeleteView):
    permission_required = ('posts.delete_post',)
    model = Post
    form_class = PostForm
    template_name = 'post_delete.html'
    success_url = reverse_lazy('home')


class ShowReplyView(PermissionRequiredMixin, ListView):
    queryset = Post.objects.filter(post__author=user).select_related('reply')
    template_name = 'replies.html'
    context_object_name = 'showreply'
    paginate_by = 10


class CreateReplyView(PermissionRequiredMixin, CreateView):
    permission_required = ('posts.add_reply',)
    model = Reply
    form_class = ReplyForm
    template_name = 'post_view.html'
    success_url = reverse_lazy('home')


class UpdateReplyView(PermissionRequiredMixin, UpdateView):
    permission_required = ('posts.update_reply',)
    model = Reply
    form_class = ReplyForm
    template_name = 'reply_update.html'
    success_url = reverse_lazy('show_reply')

    def form_valid(self, form):
        response = super().form_valid(form)

        Reply.objects.filter(id=self.object.reply_id).update(status=True)

        return response


class DeleteReplyView(PermissionRequiredMixin, DeleteView):
    permission_required = ('posts.delete_reply',)
    model = Reply
    form_class = ReplyForm
    template_name = 'reply_delete.html'
    success_url = reverse_lazy('view_post')
