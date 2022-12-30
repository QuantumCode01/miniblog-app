from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import signupform,LoginForm,PostForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Post
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

def home(request):
    post=Post.objects.all()
    return render(request,'app/home.html',{'post':post})

def about(request):
    return render(request,'app/about.html')

def contact(request):
    return render(request,'app/contact.html')

    
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
  
def user_signup(request):
    if request.method == "POST":
        form = signupform(request.POST)
        if form.is_valid():
            messages.success(request,"Congratulation !! You have become an author.")
            user=form.save()
            # Group author assigned to variable group
            group=Group.objects.get(name='Author')
            # now add user in this author group
            user.groups.add(group)
           
    else:
        form=signupform()
    return render(request, 'app/signup.html',{'form':form})

def dashboard (request):
    if request.user.is_authenticated:
        post=Post.objects.all()
        user=request.user
        # take full name of current user
        fullname=user.get_full_name()
        # take groups of current user it may be one or more
        group=user.groups.all()
        return render(request, 'app/dashboard.html',{'post':post,'fullname':fullname,'groups':group})
    else:
        return HttpResponseRedirect("/login/")


def user_login(request):
#    request.user.is_authenticated checks whther user is already logged in or not

    if not request.user.is_authenticated:
        if request.method=="POST":
            form=LoginForm(request=request,data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']

            # authenticate checks whether username and password is already stored in database ( means already user is registered) or not
                user = authenticate(request, username=uname, password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,"Logged in successfully!!")
                    return HttpResponseRedirect('/dashboard/')
    
        else:
            form= LoginForm()
        return render (request,'app/login.html',{'form':form})
    else:
        #  if already logged in go to dashboard without going to login page
        return HttpResponseRedirect('/dashboard/')



def add_post(request):
    if request.user.is_authenticated:
        if request.method =="POST":
            form=PostForm(request.POST)
            if form.is_valid():
                title= form.cleaned_data['title']
                description= form.cleaned_data['desc']
                post=Post(title=title,desc=description)
                post.save()
                messages.success(request,"Post Added Successfully!!")
                form=PostForm()
        else:
            form=PostForm()
        return render(request,'app/addpost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')


def update_post(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi=Post.objects.get(pk=id)
            form=PostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
                messages.success(request,"Post Updated Successfully!!")
                return HttpResponseRedirect('/dashboard/')
        else:
            pi=Post.objects.get(pk=id)
            form=PostForm(instance=pi)
        return render(request,'app/updatepost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

def delete_post(request,id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi= Post.objects.get(pk=id)
            pi.delete()
            messages.success(request,"Post Deleted Successfully!!")
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')
