from django.shortcuts import redirect, render
from.models import Member
from .forms import AddMemberForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm 

import requests
import json



def getWeatherdata():
    api_url = "https://weather.tsukumijima.net/api/forecast/city/140010"
    response = requests.get(api_url)
    data = response.json()
    print(data["forecasts"][0]["telop"])
    forecast = {
        'date': data["forecasts"][0]["date"].replace('-','/'),
        'telop' : data["forecasts"][0]["telop"],
        'image':data["forecasts"][0]["image"]["url"],
        'max' : data["forecasts"][0]["temperature"]["max"]["celsius"],
        'min' : data["forecasts"][0]["temperature"]["min"]["celsius"],
    }
    return forecast

@login_required
def index(request):
    query = request.GET.get('q')

    members = Member.objects.all()
    if query:
        members=members.filter(
            Q(name__icontains=query)
            |Q(age__icontains=query)
        )
    if request.GET.get('order'):
        order = request.GET.get('order')
    else:
        order = 'id'
    members = members.order_by(order)
       
    header = ['ID','name','age','変更'] 
    members = Member.objects.filter(deleted=False).all()
    weather = getWeatherdata()
    data={
        'header':header,
        'members':members,
        'order':order,
        'weather':weather,
    }
    print()
    return render(request,'my_app/index.html',data)

@login_required    
def create(request):
    # data={}
    if (request.method == 'POST'):
        form = AddMemberForm(request.POST)
        data={
            'title':'入力ページ',
            'form':form,
        }
        if form.is_valid():
            form.save()
            return redirect(to='/my_app/index')
    else:
        data={
            'title':'入力ページ',
            'form':AddMemberForm(),
        }
    return render(request,'my_app/create.html',data)

@login_required
def update(request, num):

    member_obj=Member.objects.filter(id=num,deleted=False).first()
    data={
        'title':'更新ページ',
        'id':num,

        'member':member_obj
    }
    if request.method == 'POST':
        form=AddMemberForm(request.POST, request.FILES, instance=member_obj)
        data['form']=form
        if form.is_valid():
            form.save()
            return redirect(to='/my_app/index')
    else:
        data['form']=AddMemberForm(instance=member_obj)


    return render(request,'my_app/update.html',data)

@login_required
def delete(request, num):

    member_obj=Member.objects.filter(id=num, deleted=False).first()
    if (request.method == 'POST'):
        # member_obj.deleted = True
        member_obj.image.delete(save=False)
        member_obj.image = None
        member_obj.save()
        return redirect(to='/my_app/index')
    data={
        'id':num,
        'label':['ID','名前','年齢','画像'],
        'member':member_obj,
    }
    return render(request,'my_app/delete.html',data)

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('my_app:login')
    else:
        form = SignUpForm()
    return render(request,'accounts/signup.html',{'form':form})



