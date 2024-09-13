from django.shortcuts import render
from userauths.forms import UserRegisterForm

# Create your views here.
def register_view(request):
    if request.method == "POST":
        print("USer registered successfully")
    else:
        print("USer cannot be registered")
    form = UserRegisterForm()
    
    context = {
        'form': form,
    }
    return render(request, 'userauths/signup.html', context)