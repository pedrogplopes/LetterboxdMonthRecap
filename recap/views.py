from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from .models import User
from .forms import UserForm
from django.contrib.auth import authenticate, login
from .forms import LoginForm

# Create your views here.
def index(request):
    submitted = False
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            newuser = form.save()
            print(newuser.email)
            return render(request, 'recap/index.html', {'form': form, 'submitted': True})
    else:
        form = UserForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'recap/index.html', {
        'form':form, 'submitted':submitted
    })



def login_view(request):
    error_message = None

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            lb_name = form.cleaned_data['lb_name']

            # Authenticate the user using the new backend
            user = authenticate(request, email=email, lb_name=lb_name)

            print(f"User: {user}")  # Add this line for debugging

            if user is not None:
                # If the user exists, log in the user
                login(request, user)

                # Print the email of the logged-in user
                print(f"Logged in as: {user.email}")

                # Redirect to the desired page after successful login
                return redirect('login') 
            else:
                # User not authenticated
                error_message = 'Invalid credentials. Please try again.'

    else:
        form = LoginForm()

    return render(request, 'recap/login.html', {'form': form, 'error_message': error_message})




def delete(request, email):
    if request.method == 'POST':
        try:
            user = User.objects.get(email=email)
            user.delete()
            return render(request, 'recap/deletion.html')
        except User.DoesNotExist:
            return HttpResponseBadRequest('Invalid request')
    else:
        return HttpResponseBadRequest('Invalid request method')
    