from django import forms
from django.http import HttpResponse
from django.shortcuts import render, redirect

from appAuth import models


class LoginForm(forms.Form):
    username = forms.CharField(label = 'username',
                               widget=forms.TextInput(attrs={'class': 'form-control'})
                               )
    password = forms.CharField(label = 'password',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'})
                               )


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    form = LoginForm(request.POST)
    if form.is_valid():
        # get username and password from form and check if they are valid
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = models.UserInfo.objects.filter(name=username, password=password).first()
        if user:
            # login successfully
            # generate random String as session id and save it into cookie
            request.session['user_info'] = {'id': user.id, 'name': user.name}
            # if valid, redirect to user list page
            return redirect('/users/list/')
        form.add_error('password', 'username or password is not correct')
    return render(request, 'login.html', {'form': form, 'error': 'Wrong username or password'})


def logout(request):
    request.session.clear()
    return redirect('/login/')
