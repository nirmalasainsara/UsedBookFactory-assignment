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


# create article if user login.
@login_required
def article_view(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save()
            author = Author.objects.get(user=request.user)
            article.author_set.add(author)
            return redirect(reverse("blogapp:home"))

    else:
        form = ArticleForm()
    context = {"form": form}
    return render(request, "blogapp/blogcreate.html", context)


# home page where we can check list of article.
def home_view(request):
    if request.user.is_authenticated:
        author = Author.objects.get(user=request.user)
        articles = Article.objects.exclude(author=author)
        context={"articles":articles}
        return render(request, "blogapp/home.html", context)
    else:
        articles=Article.objects.all()
        context={"articles":articles}
        return render(request, "blogapp/home.html", context)



#  article detail  
def article_detail(request, the_slug):
    article = Article.objects.get(slug=the_slug)
    authors = article.author_set.all()
    context = {"article":article, "authors":authors}
    return render(request, "blogapp/article_detail.html", context)

    
# delete article page view.
def delete_article(request, article_id):
    article= Article.objects.get(id=article_id)
    article.delete()
    return redirect(reverse("blogapp:home"))


# Edit article view
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


# user signup page for blogapp.
def signup_view(request):
    form = SignUpForm(request.POST or None) 

    if form.is_valid():  
        user = form.save(commit=False)
        password = form.cleaned_data.get('password') 
        user.set_password(password)
        user.save()
    
        new_user = authenticate(username=user.username, password=password)
        author = Author.objects.create(user=new_user)
        login(request, new_user)
        return redirect("blogapp:home")

    context = {
        "form":form
    }
    return render(request, "blogapp/blogcreate.html", context)


# user login page 
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


# The user who created article by yourself.
def user_article(request):
    author = Author.objects.get(user=request.user)
    articles = Article.objects.filter(author=author)
    context = {"articles":articles}
    return render(request, "blogapp/user_article_list.html", context)

