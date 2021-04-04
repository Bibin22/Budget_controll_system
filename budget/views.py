from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, ExpenseCreateForm,DateSearchForm, ReviewExpensForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Expence
from django.db.models import Sum

def signin(request):
    if request.method == "POST":
        uname = request.POST.get("uname")
        pwd = request.POST.get("pwd")
        user = authenticate(username=uname, password=pwd)
        if user is not None:
            login(request, user)
            return render(request, 'budget/home.html')
        else:
            return render(request, 'budget/login.html', {"messege":"invalid"})
    return render(request, 'budget/login.html')

def registration(request):
    form = UserRegistrationForm()
    context = {
        "form": form,
    }
    if request.method=="POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("signin")

        else:
            context={
                "form":form
            }
            return render(request, 'budget/registration.html', context)



    return render(request, 'budget/registration.html', context)

def signout(request):
    logout(request)

    return redirect("signin")
@login_required()
def expense_create(request):
    form = ExpenseCreateForm(initial={'user':request.user})
    context = {
        "form": form,
    }
    if request.method == 'POST':
        form = ExpenseCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('addexpense')
    return render(request, 'budget/expense.html', context)

@login_required()
def view_expense(request):
    form = DateSearchForm()
    expenses = Expence.objects.filter(user=request.user)
    context = {
        "form": form,
        "expenses":expenses
    }

    if request.method == "POST":
        form = DateSearchForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data.get("date")
            expenses = Expence.objects.filter(date=date, user=request.user)
            context = {
                "form": form,
                "expenses": expenses
            }
            return render(request, "budget/viewexpenses.html", context)
    return render(request, 'budget/viewexpenses.html', context)

@login_required()
def edit_expense(request, id):
    expenses = Expence.objects.get(id=id)
    form = ExpenseCreateForm(instance=expenses)
    context={
        'form':form,
    }
    if request.method == 'POST':
        form = ExpenseCreateForm(request.POST, instance=expenses)
        if form.is_valid():
            form.save()
            return redirect('view')
        else:
            form = ExpenseCreateForm(request.POST, instance=expenses)
            context={
                'form':form
            }
            return render(request, 'budget/edit.html', context)

    return render(request, 'budget/edit.html', context)

@login_required()
def delete_expence(request, id):
    expence = Expence.objects.get(id=id)
    expence.delete()
    return redirect('view')

def review_expense(request):
    form = ReviewExpensForm()
    context = {
        "form":form,
    }
    if request.method == "POST":
        form = ReviewExpensForm(request.POST)
        if form.is_valid():
            from_date = form.cleaned_data.get("from_date")
            to_date = form.cleaned_data.get("to_date")
            total = Expence.objects.filter(date__gte=from_date, date__lte=to_date, user=request.user).aggregate(Sum('amount'))
            total = total["amount__sum"]

            context = {
                "form":form,
                "total": total,
            }
    return render(request, 'budget/review.html', context)

