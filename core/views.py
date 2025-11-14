from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.hashers import make_password, check_password

from .models import User, Role
from utils.validators import email_validator, password_validator

def show_login_page(request: HttpRequest):
    if request.method == "GET":
        if request.COOKIES.get('email') is not None:
            return redirect('/core/home')
        
        return render(request, 'login.html')
    return login(request)

def login(request: HttpRequest):
    email = request.POST.get('email')
    password = request.POST.get('password')

    if email is None or password is None:
        return render (request, 'login.html',{
            "error" : "Email and Password are compulsory"
        })
    
    user = User.objects.filter(email=email).first()
    if user is None:
        return render(request, 'login.html' , {
            "error" : "Wrong email or password"
        })
    
    is_pass_valid = check_password(password, user.password_hash)
    if not is_pass_valid:
        return render(request, 'login.html' , {
            "error" : "Wrong email or password"
        })
    
    response = redirect("/core/home")
    response.set_cookie(key='email', value=email)
    return response

def show_signup_page(request: HttpRequest):
    if request.method == "GET":
        if request.COOKIES.get('email') is not None:
            return redirect('/core/home')
        
        return render(request, 'signup.html')
    return signup(request)

def signup(request: HttpRequest):
    email = request.POST.get('email')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')

    if email is None or password is None or confirm_password is None:
        return render(request, 'signup.html', {
            "error" : "All fields are necessary"
        })
    
    if password != confirm_password:
        return render(request, 'signup.html', {
            "error" : "Passwords doesn't match"
        })
    
    is_email_valid = email_validator.validate(email)
    if not is_email_valid:
        return render(request, 'signup.html', {
            "error" : "Email is not valid"
        })
    
    is_pass_valid = password_validator.validate(password)
    if not is_pass_valid:
        return render(request, 'signup.html', {
            "error" : "Password must contain atleast 8 characters and atleast one of a capital letter, small letter, number and a special character."
        })
    
    existing = User.objects.filter(email=email)
    if existing.count() > 0:
        return render(request, 'signup.html', {
            "error" : "This email is already registered"
        })

    customer_role = Role.objects.filter(name="Customer").first()

    user = User()
    user.email = email
    user.password_hash = make_password(password)
    user.role = customer_role
    user.save()

    return render(request, 'signup.html', {
        "success" : "Registered Successfully!"
    })

def logout(request: HttpRequest):
    response = redirect('/core/login')
    response.delete_cookie('email')
    
    return response

def show_home_page(request: HttpRequest):
    if request.COOKIES.get('email') is None:
        return redirect('/core/login')
    
    return render(request, 'home.html')