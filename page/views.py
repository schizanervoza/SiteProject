from django.shortcuts import render

# Create your views here.
from django.http import *
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import redirect
from .forms import *



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            if form.get_user() and form.get_password():
                user = User.objects.create_user(username=form.get_user(),password=form.get_password())
                user.save()
                login(request, user)
            return HttpResponseRedirect('/')
    
    else:
        form = RegistrationForm()
    return render(request, 'page/register.html', {'form': form})
    
@login_required(login_url='/login/')
def main(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'page/main.html', {'posts': posts})


def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            if form.get_user():
                login(request, form.get_user())
                return HttpResponseRedirect('/')
    else:
        form = LoginForm()
    return render(request, 'page/login.html', {'form': form})

@login_required(login_url='page/login/')
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['fake'] =='':
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('/')
    else:
        form = PostForm()
    form = PostForm()
    return render(request, 'page/new_post.html', {'form': form})