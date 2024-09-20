from django.shortcuts import redirect, render
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib import messages
from django.conf import settings

User = get_user_model()

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
    # If the user is already logged in
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect("core:index")
    
    # Handle POST requests (when login form is submitted)
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try: 
           user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.warning(request, f"User with {email} does not exist")
            form = UserRegisterForm()  # Pass registration form back
            return render(request, "userauths/signup.html", {'form': form})  # Re-render with form
        
        # Authenticate user with provided credentials
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You are logged in")
            return redirect("core:index")
        else:
            messages.warning(request, "Incorrect credentials, please try again.")
            form = UserRegisterForm()  # Pass registration form back
            return render(request, "userauths/signup.html", {'form': form})  # Re-render with form
    
    # If it's a GET request (render the login page)
    form = UserRegisterForm()  # Registration form
    return render(request, "userauths/signup.html", {'form': form})  



def logout_view(request):
    logout(request)
    messages.success(request, "You have logged out")
    return redirect("userauths:signin")