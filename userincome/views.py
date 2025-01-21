import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from expenses.models import Category, Expense
from django.core.paginator import Paginator

from userincome.models import Source, UserIncome
from userpreferences.models import UserPreferences

def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        income = UserIncome.objects.filter(amount__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            date__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            description__icontains=search_str, owner=request.user) | UserIncome.objects.filter(
            source__icontains=search_str, owner=request.user)
        data = income.values()
        return JsonResponse(list(data), safe=False)
    
    
@login_required(login_url='authentication/login')
def index(request):
    income = UserIncome.objects.filter(owner=request.user)  
    paginator = Paginator(income, 2)  
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreferences.objects.get(user=request.user).currency
    context = {
        'income': income,
        'page_obj': page_obj,
        'currency': currency,
    }
    return render(request, 'userincome/index.html',context)

def add_income(request):
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'userincome/add_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Income is required')
            return render(request, 'userincome/add_income.html', context)
        description = request.POST['description']
        date = request.POST['date']
        source = request.POST['source']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'userincome/add_income.html', context)

        UserIncome.objects.create(owner=request.user, amount=amount, date=date, source=source, description=description)
        messages.success(request, 'Income saved successfully')

        return redirect('income')
    
def edit_income(request, id):
    income = UserIncome.objects.get(pk=id)
    sources = Source.objects.all()
    context ={
        'income': income,
        'values': income,
        'sources': sources
    }
    if request.method == 'GET':
        return render(request, 'userincome/edit_income.html', context)
    
    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'userincome/edit_income.html', context)
        description = request.POST['description']
        date = request.POST['date']
        source = request.POST['source']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'userincome/edit_income.html', context)

        income.amount = amount
        income. date = date
        income.source = source
        income.description = description

        income.save()
        messages.success(request, 'income Updated successfully')

        return redirect('income')
    
    
def delete_income(request, id):
    income= UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request, 'income removed')
    return redirect('income')