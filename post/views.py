from django.shortcuts import render,redirect
from django.views import generic
from django.views.generic import View
from post.models import Post
from post.forms import PostForm
# Create your views here.
class HomeView(generic.ListView):
    template_name='post/index.html'
    model=Post

class CreatePostView(View):
    # template_name='post/create_post.html'
    # model=Post
    # success_url='/'
    def get(self,request):
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

class DetailPostView(generic.DetailView):
    model=Post
    template_name='post/detail_post.html'

class UpdatePostView(View):
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
            post.author=form.cleaned_data.get('author')
            post.title = form.cleaned_data.get('title')
            post.image = form.cleaned_data.get('image')
            post.content = form.cleaned_data.get('content')
            post.created_date = form.cleaned_data.get('created_date')
            post.save(update_fields=['author','title','image','content','created_date'])
            return redirect('/')





