from django.shortcuts import render, redirect, reverse
from .models import Author, Article
from .forms import ArticleForm, AuthorForm, SignUpForm, LoginForm
from django.contrib.auth import(
    authenticate,
    get_user_model,
    login,
    logout,
)
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required


def article_view(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("blogapp:home"))

    else:
        form = ArticleForm()
    context = {"form": form}
    return render(request, "blogapp/blogcreate.html", context)

def home_view(request):
    articles = Article.objects.all()
    context={"articles":articles}
    return render(request, "blogapp/home.html", context)


def article_detail(request, the_slug):
    article = Article.objects.get(slug=the_slug)
    authors = article.author_set.all()
    context = {"article":article, "authors":authors}
    return render(request, "blogapp/article_detail.html", context)

def author_view(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("blogapp:home"))

    else:
        form = AuthorForm()
    context = {"form": form}
    return render(request, "blogapp/blogcreate.html", context)



def delete_article(request, article_id):
    article= Article.objects.get(id=article_id)
    article.delete()
    return redirect(reverse("blogapp:home"))


def update_article(request,article_id):
    article = Article.objects.get(id=article_id)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect(reverse("blogapp:home"))
        return render(request, "blogapp/blogcreate.html", {"article": article, "form": form})
    
    else:
        form = ArticleForm(instance=article)
        return render(request, "blogapp/blogcreate.html", {"article": article, "form": form})

def signup_view(request):
    form = SignUpForm(request.POST or None) 
    if form.is_valid():  
        user = form.save(commit=False)
        password = form.cleaned_data.get('password') 
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        return redirect("blogapp:home")

    context = {
        "form":form
    }
    return render(request, "blogapp/blogcreate.html", context)


def login_view(request):
    form = LoginForm(request.POST or None) 
    if form.is_valid():  
        username = form.cleaned_data.get('username') 
        password = form.cleaned_data.get('password') 
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect(reverse("blogapp:home"))
    return render(request, "blogapp/blogcreate.html", {"form":form})



def logout_view(request):
    logout(request)
    return redirect(reverse("blogapp:home"))