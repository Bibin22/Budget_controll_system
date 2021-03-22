
from django.urls import path
from django.shortcuts import render
from .views import registration, signin, signout, expense_create, view_expense, edit_expense, delete_expence, review_expense
urlpatterns = [
    path("", lambda request:render(request, "budget/base.html")),
    path("register", registration, name='registration'),
    path("signin", signin, name='signin'),
    path("signout", signout, name="signout"),
    path("addexpense", expense_create, name="addexpense"),
    path("view", view_expense, name='view'),
    path('edit<int:id>', edit_expense, name='edit'),
    path('delete<int:id>', delete_expence, name='delete'),
    path('review', review_expense, name='review')
]
