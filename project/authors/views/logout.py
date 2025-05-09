from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


@login_required(login_url="authors:login", redirect_field_name="next")
def logout_view(request):
    if not request.POST:
        messages.error(request, "Invalid logout request")
        return redirect(reverse("authors:login"))

    if request.POST.get("username") != request.user.username:
        messages.error(request, "Invalid logout user")
        return redirect(reverse("authors:login"))

    messages.success(request, "Logged out successfully")
    logout(request)
    return redirect(reverse("authors:login"))
