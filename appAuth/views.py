from django.http import HttpResponse
from django.shortcuts import render, redirect
from appAuth import models


# Create your views here.

def index(request):
    return HttpResponse("You're at the appAuth index.")


def user_list(request):
    user_info = request.session.get('user_info')
    current_user = models.UserInfo.objects.filter(id=user_info['id']).first()
    if current_user.get_user_type_display() == 'Admin':
        print("admin")
        # get users data from database
        users = models.UserInfo.objects.filter(company_id=current_user.company_id).all()
        return render(request, 'user_list.html', {'users': users})
    return render(request, 'userpage.html')


def user_edit(request, nid):
    if request.method == "GET":
        user = models.UserInfo.objects.filter(id=nid).first()
        # each person in one company has only one credit card
        credit_card = models.Credit_card.objects.filter(host=user).first()  # get credit card info

        return render(request, 'user_edit.html', {'user': user, 'credit_card': credit_card})
    new_limit = request.POST.get('limit')
    card = models.Credit_card.objects.filter(host_id=nid).first()
    # current balance should always be smaller than limit
    if float(new_limit)<card.curr_balance:
        models.Credit_card.objects.filter(host_id=nid).update(curr_balance=float(new_limit))
    models.Credit_card.objects.filter(host_id=nid).update(limit=new_limit)


    return redirect('/users/list/')

def user_info(request):
    if request.method == "GET":
        # get user info from session
        user_info = request.session.get('user_info')
        current_user = models.UserInfo.objects.filter(id=user_info['id']).first()
        return render(request, 'user_info.html', {'current_user': current_user})


def card_info(request):
    if request.method == "GET":
        current_user = request.session.get('user_info')
        card = models.Credit_card.objects.filter(host=current_user['id']).first()

        return render(request, 'card_info.html', {'card': card})


