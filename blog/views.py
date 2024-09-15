from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Post  # Make sure the Post model is defined in models.py
from .forms import PostForm  # Ensure that PostForm is defined in forms.py
from django.shortcuts import render
from django.db import connection

def sql_results(request):
    query = "SELECT * FROM blog_post"  # Замените 'myapp_post' на имя вашей таблицы
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    # Здесь вы можете настроить, чтобы отображать результат в более удобном формате
    posts = [{"id": row[0], "title": row[1], "content": row[2]} for row in rows]
    
    return render(request, 'sql_results.html', {'posts': posts})

def index(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def home(request):
    posts = Post.objects.all()
    form = PostForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('home')

    return render(request, 'home.html', {'posts': posts, 'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

from .models import BlogPost


