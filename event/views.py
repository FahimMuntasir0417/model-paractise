from django.shortcuts import render
from .forms import categoryForm
from .models import Category ,Event, Participant
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect, get_object_or_404    

# Create your views here.
def create_category(request):
    if request.method == 'POST':
        form = categoryForm(request.POST)
        if form.is_valid():
            form.save()
            # return render(request, 'event/category_success.html', {'form': form})
    else:
        form = categoryForm()
    return render(request, 'event/create_category.html', {'form': form, 'title': 'Create Category'})

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import authenticate, login

# def signup_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         email = request.POST['email']
#         password1 = request.POST['password1']
#         password2 = request.POST['password2']

#         if password1 != password2:
#             messages.error(request, "Passwords do not match.")
#             return redirect('signup')

#         if User.objects.filter(username=username).exists():
#             messages.error(request, "Username already taken.")
#             return redirect('signup')

#         if User.objects.filter(email=email).exists():
#             messages.error(request, "Email already in use.")
#             return redirect('signup')

#         user = User.objects.create_user(username=username, email=email, password=password1 ,is_active=False)
#         login(request, user)
#         messages.success(request, "Account created successfully!")
#         return redirect('dashboard')  # Replace with your desired redirect

#     return render(request, 'signup.html')

  # Make sure this is correct path
from .signals import send_activation_email

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use.")
            return redirect('signup')

        # Create user with is_active=False
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.is_active = False
        user.save()

        # Send activation email
        send_activation_email(user, request)

        messages.success(request, "Account created! Please check your email to activate your account.")
        return redirect('login')  # Don't log in yet, wait for activation

    return render(request, 'signup.html')

def dashboard_view(request):
    return render(request, 'dashboard.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect('dashboard')  # replace with actual view name
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'login.html')

def activate(request, uid, token):
    user = get_object_or_404(User, pk=uid)
    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Account activated!")
        return redirect('login')  # Replace with your desired redirect
    else:
        messages.error(request, "Activation link is invalid!")
        return redirect('signup')