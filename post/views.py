from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
# generic.ListView=
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from django.views.generic import View
from post.models import Post, Comment
from post.forms import PostForm, CommentForm
from my_blog_class_base.db_connection  import BlogApi
from django.http import HttpResponse



# Create your views here.
# class HomeView(ListView):
class HomeView(View):
    template_name='post/index.html'
    model=Post
# here paginate
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

# contains detail view and Comment view
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

class UpdatePostView(LoginRequiredMixin,UpdateView):
    # login_url='/login'
    template_name = 'post/update_post.html'
    form_class = PostForm
    model=Post
    # class UpdateView  has inbuilt get/ post
    def get(self, request, *args, **kwargs):
    # from url page get the <int:pk> below code
        pk = self.kwargs['pk']
        post = Post.objects.get(pk=pk)
        # below is an object
        user = request.user
        author = post.author
        # below both are object
        if user == author:
            # whatever is in get () in class UpdateView override that with this func
            # super() function represents the parent class of the current one in this case, TemplateView
            # and will output whatever it would this modified get() would want.
            return super().get(request, *args, **kwargs)
        else:
            message = "You can only update the post you have written."
            return render(request, 'post/message.html',{"comment_update": message})
    # class UpdateView has
    def post(self, request, *args, **kwargs):
        # from url page get <int:pk> below code
        pk = kwargs.get('pk')
        # after success send it to below url
        self.success_url = f'/detail_post/{ pk }'
        # below updates the get which is from Class UpdateView implicitly + db commit
        return super().post(request, *args, **kwargs)
    #
class DeletePostView(LoginRequiredMixin,DeleteView):
    model=Post
    template_name = "post/delete_post.html"
    success_url='/'
    # overriding the default inbuilt get (self, request, *args, **kwargs) of DeleteView Class
    def get(self,request, *args, **kwargs):
        pk=self.kwargs['pk']
        post=Post.objects.get(pk=pk)
        user=request.user
        author=post.author
        # below r objects
        if user==author:
           # u don't need to delete when u do 'get'; u r just modifying the get with author, user comparison
           return super().get(request, *args, **kwargs)
        else:
            message="you can only delete the post You have written"
            return render(request, 'post/message.html',{'post_update':message})
    def post(self, request, *args, **kwargs):
        self.success_url='/'
        # deleteView has object.Delete() inside its post method
        return super().post(request, *args, **kwargs)

class UpdateCommentView(LoginRequiredMixin, UpdateView):
    template_name = 'post/detail_post.html'
    form_class = CommentForm
    queryset = Comment.objects.all()
    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        context = super().get_context_data(**kwargs)
        comment = Comment.objects.get(pk=pk)

        post = comment.post
        context['post'] = post
        context['posts'] = Comment.objects.filter(post=post)
        return context

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        comment = Comment.objects.get(pk=pk)

        user = request.user
        commentor = comment.commentor
        if user== commentor:
            return super().get(request, *args, **kwargs)
        else:
            message = "You can only update the comment you have written."
            return render(request, 'post/message.html', {"comment_update": message})

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        comment = get_object_or_404(Comment, pk=pk)
        post_pk = comment.post.pk
        self.success_url = f'/detail_post/{ post_pk }'
        return super().post(request, *args, **kwargs)


class DeleteCommentView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        pk = kwargs.get('pk')
        comment = get_object_or_404(Comment, pk=pk)
        # commentor type is objec type eventhough commentor looks like attribute of Comment
        commentor = comment.commentor


        post_pk = comment.post.pk
        if user == commentor:
            comment.delete()
            return redirect(f'/detail_post/{ post_pk }')
        else:
            message = "You can only delete the comment you have written."
            return render(request, 'post/message.html', {"comment_delete": message})

def populate_post(request):
    if request.method=="GET":
        blogApiObject= BlogApi()
        blogApiObject.populate()
        return HttpResponse("Successfully populated the post from PostgreSQL")
