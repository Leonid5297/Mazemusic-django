from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, reverse, redirect
from .forms import UserRegistrationForm, UserLoginForm, ProfileForm
from django.http import HttpResponseRedirect
from django.views import View


# Create your views here.


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                messages.success(request, f"{username}, Вы вошли в аккаунт")

                redirect_page = request.POST.get('next', None)
                if redirect_page and redirect_page != reverse('logout'):
                    return HttpResponseRedirect(request.POST.get('next'))

                return HttpResponseRedirect(reverse('main_page'))
    else:
        form = UserLoginForm()

    context = {
        'title': 'Home - Авторизация',
        'form': form
    }
    return render(request, 'users/login.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()

            session_key = request.session.session_key

            user = form.instance
            auth.login(request, user)

            messages.success(request, f"{user.username}, Вы успешно зарегистрированы и вошли в аккаунт")
            return HttpResponseRedirect(reverse('main_page'))
    else:
        form = UserRegistrationForm()

    context = {
        'title': 'Home - Регистрация',
        'form': form
    }
    return render(request, 'users/registration.html', context)


class UserProfileView(View):
    def get(self, request):
        form = ProfileForm(instance=request.user)  # отображается информация, которая числится за юзером
        return render(request, 'users/profile.html', context={'form': form, })

    def post(self, request):
        form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)  # для какого юзера сохраняем
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile'))

        return render(request, 'users/profile.html', context={'form': form, })

@login_required
def logout(request):
    messages.success(request, f"{request.user.username}, Вы вышли из аккаунта")
    auth.logout(request)
    return redirect(reverse('main_page'))


def redirect_admin(request):
    return HttpResponseRedirect('http://127.0.0.1:8000/admin/')
