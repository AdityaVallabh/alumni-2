from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, reverse, render
from django.conf import settings
import django.forms as forms

def health(request):
    return HttpResponse("Hello world. I'm up and running.")


def signup(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = User.objects.create_user(username, email, password)
    user.save()
    return HttpResponse('Done!')


class LoginForm(forms.Form):
    username = forms.CharField(label='username')
    password = forms.CharField(label='password', widget=forms.PasswordInput)

    username.widget.attrs.update({'class': 'form-control'})
    password.widget.attrs.update({'class': 'form-control'})


def login_view(request):
    if request.method == "GET":
        return render(request, 'login.html', {'form': LoginForm()})

    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is None:
        return HttpResponse('Incorrect creds')
    else:
        login(request, user)
        return redirect('/portal/{}'.format(username))


def logout_route(request):
    logout(request)
    return redirect('/')


def requires_auth(request):
    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format(reverse(login_view), request.path))
    else:
        return HttpResponse('You are authorized.')


@login_required
def test_authorized(request):
    return HttpResponse('Authorized success.')
