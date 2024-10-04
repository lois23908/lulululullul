from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

def signup(request):

    if request.method == 'POST':
       print(request.POST)
       username = request.POST.get('username')
       firstname = request.POST.get('fname')
       lastname = request.POST.get('lname')
       email = request.POST.get('email')
       pass1 = request.POST.get('pass1')
       pass2 = request.POST.get('pass2')

       if pass1 != pass2:
            messages.error(request, "Passwords do not match.")
            return render(request, "authentication/signup.html")
       
       if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose a different username.")
            return render(request, "authentication/signup.html")
       if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return render(request,"authentication/signup.html")
       if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return render(request,"authentication/signup.html")

       myuser = User.objects.create_user(username, email, pass1)
       myuser.first_name = firstname
       myuser.last_name = lastname

       myuser.save()

       messages.success(request, "Your Account has been successfully created.")
       return redirect('signin')

    return render(request, "authentication/signup.html")

def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            firstname = user.first_name
            return render(request, "authentication/index.html", {'firstname': firstname})

        else:
            messages.error(request, "Bad Credentials!")
            return render(request, "authentication/signin.html")

    return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully")
    return redirect('home')