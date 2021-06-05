from django import forms

from .models import Article, Author

from django.contrib.auth import(
    authenticate,
    get_user_model,
    login,
    logout,
    
)
User = get_user_model()


# Article form
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = (
            "title",
            "description",
        )


# Author form
class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = "__all__"


# user signup form
class SignUpForm(forms.ModelForm): 
    email = forms.EmailField(label='Email Address')
    email2 = forms.EmailField(label='Confirm Email')
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password'
        ]

    def clean_email2(self,*args, **kwargs):
        email = self.cleaned_data.get('email') 
        email2= self.cleaned_data.get('email2') 
        if email != email2:
            raise forms.ValidationError("Email must match")
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("This email has already been registered")
        return email


# user login form
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self,*args, **kwargs):
        username = self.cleaned_data.get('username') 
        password = self.cleaned_data.get('password') 
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("this user does not exit")
            if not user.check_password(password):    
                raise forms.ValidationError("incorrect password")
            if not user.is_active:
                raise forms.ValidationError("this user is not longer active")
        return super(LoginForm, self).clean(*args,**kwargs)
    