from django.contrib import admin
from django.urls import path
from . import views

app_name = "blogapp"

urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('createblog/', views.article_view, name='createblog'),
    path('article_detail/<slug:the_slug>', views.article_detail, name='article_detail'),
    path("update/<int:article_id>/", views.update_article, name="update"),
    path("delete/<int:article_id>/", views.delete_article, name="delete"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("user_article/", views.user_article, name="user_article"),
    
]

