from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
# generic.ListView=
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic import View
from post.models import Post, Comment
from post.forms import PostForm, CommentForm
# Create your views here.
class HomeView(ListView):
    template_name='post/index.html'
    model=Post

class CreatePostView(LoginRequiredMixin,View):
    # accounts / login
    # login_url='/login'
    def get(self,request):
        user=request.user
        context={}
        form=PostForm()
        context['form']=form
        return render(request,template_name='post/create_post.html',context=context)
    def post(self,request):
        form=PostForm(request.POST)
        if form.is_valid():
            author=request.user
            title=form.cleaned_data.get('title')
            image=form.cleaned_data.get('image')
            content=form.cleaned_data.get('content')
            post=Post(author=author, title=title,image=image,content=content)
            post.save()
            return redirect('/')

class DetailPostView(LoginRequiredMixin,DetailView):
    # login_url='/login'
    model=Post
    template_name='post/detail_post.html'

    def get(self, request, *args, **kwargs):
        context={}
        context['form']=CommentForm()
        pk=kwargs.get('pk')
        post=Post.objects.get(pk=pk)
        # pass the context of the Post object 'post' as you need the post to be populated in the page
        # and then registered user can comment on the specifice post.
        context['post']=post
        # below one posts is the reverse relationship for post which links to Comment Class via FK
        context['posts']=Comment.objects.filter(post=post)

        return render(request, template_name="post/detail_post.html", context=context)

    def post(self, request, *args, **kwargs):
        commentor = request.user
        pk=kwargs.get('pk')
        post = Post.objects.get(pk=pk)

        form = CommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            comment = Comment(commentor=commentor, post=post, content=content)
            comment.save()
            # redirect to same page
            return redirect(request.path_info)

class UpdatePostView(LoginRequiredMixin,View):
    # login_url='/login'
    def get(self,request,pk):
        context={}
        author=request.user
        post=Post.objects.get(id=pk)
        data={'author':author,'title':post.title,'image':post.image,'content':post.content,'created_date':post.created_date}
        form=PostForm(data)
        context['form']=form
        return render(request, template_name="post/update_post.html",context=context)

    def post(self, request,pk):
        post= Post.objects.get(id=pk)
        form=PostForm(request.POST)
        if form.is_valid():
            post.title = form.cleaned_data.get('title')
            post.image = form.cleaned_data.get('image')
            post.content = form.cleaned_data.get('content')
            post.save(update_fields=['author','title','image','content'])
            return redirect('/')

class DeletePostView(LoginRequiredMixin,DeleteView):
    model=Post
    template_name = "post/delete_post.html"
    success_url='/'



