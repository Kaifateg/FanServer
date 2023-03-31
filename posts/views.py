from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy

from .filters import PostFilter
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
        pass

        # return render(request, 'post.html', {'post_form': post_form})


class HomePageView(ListView):
    queryset = Post.objects.all()
    template_name = 'home.html'
    ordering = '-time_create_post'
    context_object_name = 'homepage'
    paginate_by = 10


class PostView(DetailView):
    queryset = Post.objects.all()
    template_name = 'post_view.html'
    context_object_name = 'post_view'


class CreatePostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post.html'
    success_url = reverse_lazy('home')


class UpdatePostView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_update.html'
    success_url = reverse_lazy('home')


class DeletePostView(DeleteView):
    model = Post
    form_class = PostForm
    template_name = 'post_delete.html'
    success_url = reverse_lazy('home')


class ShowReplyView(ListView):
    queryset = Post.objects.filter(author=user).select_related('reply')
    template_name = 'replies.html'
    context_object_name = 'show_reply'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class AuthorReplyView(DetailView):
    queryset = Reply.objects.filter(author=user, status=True)
    template_name = 'author_reply.html'
    context_object_name = 'author_reply'
    paginate_by = 10


class CreateReplyView(CreateView):
    model = Reply
    form_class = ReplyForm
    template_name = 'post_view.html'
    success_url = reverse_lazy('home')


class UpdateReplyView(UpdateView):
    model = Reply
    form_class = ReplyForm
    template_name = 'reply_update.html'
    success_url = reverse_lazy('show_reply')

    def form_valid(self, form):
        response = super().form_valid(form)

        Reply.objects.filter(id=self.object.reply_id).update(status=True)

        return response


class DeleteReplyView(DeleteView):
    model = Reply
    form_class = ReplyForm
    template_name = 'reply_delete.html'
    success_url = reverse_lazy('view_post')
