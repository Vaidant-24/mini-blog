from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from blog.forms import SignUpForm,LoginForm,PostForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Group
from blog.models import Post
from django.urls import reverse
# Create your views here.
def index(request):
    posts = Post.objects.all()
    return render(request, 'blog/index.html',{'posts': posts})

def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    return render(request, 'blog/contact.html')

def dashboard(request):
    if request.user.is_authenticated:
        posts  = Post.objects.all()
        user = request.user
        name = user.get_username()
        gps = user.groups.all()
        return render(request, 'blog/dashboard.html', {'posts': posts,'name':name,'groups': gps})
    else:
        return HttpResponseRedirect(reverse('blog:logout'))

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form  = LoginForm(request = request , data = request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                pwd  = form.cleaned_data['password']
                user = authenticate(username = uname, password = pwd)
                if user is not None:
                    login(request, user)
                    messages.success(request,'User Logged-in Successfully!!!')
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request,'blog/login.html',{'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')

def user_logout(request):
    logout(request)
    messages.success(request,"User Logged-out Successfully!!!")
    return HttpResponseRedirect('/')

def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request,"Congratulations!!! You are now an Author")
            user = form.save()
            group  = Group.objects.get(name = "Author")
            user.groups.add(group)
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html' ,{'form':form})

def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                pst  = Post(title=title, desc=desc)
                pst.save()
                messages.success(request,"Post Added Successfully!!!")
                return HttpResponseRedirect(reverse('blog:dashboard'))
        else:
            form = PostForm()
        return render(request, 'blog/addpost.html', {'form': form})
    else:
        return render(request, 'blog/login.html')
    
def update_post(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            obj = Post.objects.get(id=id)
            fm = PostForm(request.POST , instance=obj)
            if fm.is_valid():
                fm.save()
                messages.success(request,"Post Updated Successfully!!!")
                return HttpResponseRedirect(reverse('blog:dashboard'))
        else:
            obj = Post.objects.get(id = id)
            fm = PostForm(instance = obj)
        return render(request, 'blog/updatepost.html', {'fm':fm})
    else:
        return render(request, 'blog/login.html')
    
def delete_post(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = Post.objects.get(id=id)
            fm.delete()
            messages.success(request,"Post Delete Successfully!!!")
            return HttpResponseRedirect(reverse('blog:dashboard'))
    else:
        return render(request, 'blog/login.html')
      
        