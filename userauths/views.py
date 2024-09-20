from django.shortcuts import redirect, render
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your views here.
def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Hey {username} your account was created succesfully"),
            new_user = authenticate(username=form.cleaned_data['email'],
            password = form.cleaned_data["password1"] 
            )
            login(request, new_user)
            return redirect("core:index")
        
    else:
        print("USer cannot be registered")
        form = UserRegisterForm()
    
    
    context = {
        'form': form,
    }
    return render(request, 'userauths/signup.html', context)

def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect("core:index")
    
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try: 
           user = User.objects.get(email=email)
        except:
            messages.warning(request, f"User with {email} does not exist")
        
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You are logged in")
            print("Logined innn")
            return redirect("core:index")
        else:
            messages.warning(request, "USer does not exists, Create an Account")
        
        # context = {
            
        # }
            
    return render(request, "userauths/signin.html")


def logout_view(request):
    logout(request)
    messages.success(request, "You have logged out")
    return redirect("userauths:signup")