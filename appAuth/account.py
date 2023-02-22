from io import BytesIO

from django import forms
from django.http import HttpResponse
from django.shortcuts import render, redirect

from appAuth.utils.verify_code import check_code
from appAuth import models

class LoginForm(forms.Form):
    username = forms.CharField(label='username',
                               widget=forms.TextInput(attrs={'class': 'form-control'})
                               )
    password = forms.CharField(label='password',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'})
                               )
    # Drop-down menu - select company
    # options is "ANZ" and "CBA"
    # get the value of the selected options from database

    queryset = models.Company.objects.all()
    temp_list = []
    # get company name from queryset
    for item in queryset:
        id = item.id
        name = item.name
        temp_list.append((id, name))
    # convert to tuple
    company_list = tuple(temp_list)

    company = forms.ChoiceField(label='company',
                                choices=company_list,
                                widget=forms.Select(attrs={'class': 'form-control'})
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
        company = form.cleaned_data['company']
        # we already assume that each username in a company is unique
        user = models.UserInfo.objects.filter(name=username, password=password, company=company).first()

        if user:
            # login successfully
            # generate random String as session id and save it into cookie
            # get company name based on company id
            company_name = models.Company.objects.filter(id=user.company_id).first()
            print(CODE)

            request.session['user_info'] = {'id': user.id, 'name': user.name, 'company': str(company_name), 'company_id': user.company_id}
            # if valid, redirect to user list page
            return redirect('/users/list/')
        form.add_error('password', 'Information is not correct')
    return render(request, 'login.html', {'form': form, 'error': 'Wrong username or password'})


def logout(request):
    request.session.clear()
    return redirect('/login/')


def get_image_code(request):
    img, code = check_code()
    # save as bytesIO
    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue(), {'code': code})