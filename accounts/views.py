from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from .forms import RegisterForm, LoginForm
from .models import Customer

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created. Please log in.")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data["identifier"]
            password = form.cleaned_data["password"]
            user = None
            if "@" in identifier:
                try:
                    user_obj = Customer.objects.get(email__iexact=identifier)
                    user = authenticate(request, username=user_obj.username, password=password)
                except Customer.DoesNotExist:
                    pass
            else:
                try:
                    user_obj = Customer.objects.get(phone=identifier)
                    user = authenticate(request, username=user_obj.username, password=password)
                except Customer.DoesNotExist:
                    user = authenticate(request, username=identifier, password=password)
            if user:
                login(request, user)
                return redirect(request.GET.get("next", "/"))
            messages.error(request, "Invalid login details.")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("/")
