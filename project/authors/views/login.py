from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from project.authors.forms import LoginForm
from django.http import Http404
from django.contrib.auth import authenticate, login


def login_view(request):
    form = LoginForm()
    return render(request, "authors/pages/login.html", {
        "form": form,
        "form_action": reverse("authors:login_create")
    })


def login_create(request):
    if not request.POST:
            raise Http404()
    
    form = LoginForm(request.POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username = form.cleaned_data.get("username", ""),
            password = form.cleaned_data.get("password", "")
        )

        if authenticated_user is not None:
            messages.success(request, "You are logged in")
            login(request, authenticated_user)
        else:
            messages.error(request, "Invalid credentials")
    else:
        messages.error(request, "Invalid username or password")
    
    return redirect(reverse("authors:dashboard"))
