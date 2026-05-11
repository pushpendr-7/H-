from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, LoginForm


def home_redirect(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return redirect("signup")


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = "django.contrib.auth.backends.ModelBackend"
            login(request, user)
            messages.success(request, f"Welcome {user.get_full_name()}! Account ban gaya.")
            return redirect("dashboard")
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    error = None

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=email, password=password)

            if user is not None and user.is_active:
                user.backend = "django.contrib.auth.backends.ModelBackend"
                login(request, user)
                messages.success(request, f"Login ho gaye! Welcome back, {user.get_full_name()}.")
                return redirect("dashboard")
            else:
                error = "Email ya password galat hai. Dobara try karo."
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form, "error": error})


def logout_view(request):
    logout(request)
    messages.info(request, "Aap logout ho gaye hain.")
    return redirect("login")


@login_required
def dashboard_view(request):
    return render(request, "accounts/dashboard.html", {"user": request.user})
