from django.contrib import messages
from project.authors.forms import RegisterForm
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse


def register_view(request):
    register_form_data = request.session.get("register_form_data", None)
    form  = RegisterForm(register_form_data)
    return render(request, "authors/pages/register_view.html", {
        "form": form,
        "form_action": reverse("authors:register_create")
    })


def register_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session["register_form_data"] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, "Your user is created, please login")
        del(request.session["register_form_data"])
        return redirect(reverse("authors:login"))


    return redirect("authors:register")