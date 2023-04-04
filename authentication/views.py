from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from . import forms

""" Function Based Views for authentication """


def login_page(request):
    form = forms.LoginForm()  # we include the connection form
    message = ''
    if request.method == 'POST':  # check the request type
        form = forms.LoginForm(request.POST)
        if form.is_valid():  # this method results in validation and cleaning of the form data
            user = authenticate(
                username=form.cleaned_data['username'],  # after the validation process,
                password=form.cleaned_data['password'],  # Django returns a dictionary which contains cleaned data
            )  # the authenticate function checks if the username and the password are valid
            if user is not None:  # if it is valid then it returns the corresponding user
                login(request, user)  # connection of the user
                return redirect('feed')  # we redirect the user to the feed page using a name of view
            else:
                message = 'Identifiants invalides.'
    return render(
        request, 'authentication/home.html', context={'form': form, 'message': message})
# the context contains the data we will use in the template


def logout_user(request):
    logout(request)  # to logout we just need to use the Django built-in function logout
    return redirect('home')


def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)  # a new user is created via the form
        if form.is_valid():
            user = form.save()   # save it in the database
            # auto-login user
            login(request, user)
            return redirect('feed')
    return render(request, 'authentication/signup.html', context={'form': form})
