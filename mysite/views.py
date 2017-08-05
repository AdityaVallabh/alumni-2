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


def login_view(request):
    if request.method == "GET":
        return render(request, 'login.html', {'form': LoginForm()})

    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=pclass LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)


class User_BasicInfoForm(ModelForm):
    class Meta:
        model = User
        fields = ['roll_no', 'name', 'email_1', 'date_of_birth', 'gender']


class User_MiscInfoForm(ModelForm):
    class Meta:
        model = User
        fields = ['email_2', 'phone_1', 'phone_2', 'marital_status',
                  'blood_group', 'photograph', 'nationality',
                  'permanent_address', 'scope_permanent_address',
                  'current_address', 'scope_current_address']


class User_SocialLinksForm(ModelForm):
    class Meta:
        model = User
        fields = ['link_facebook', 'scope_facebook',
                  'link_twitter', 'scope_twitter',
                  'link_linkedin', 'scope_linkedin',
                  'link_skype', 'scope_skype',
                  'link_github', 'link_blog', 'link_website']


class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
        # set user_roll_no as hidden


class QualificationForm(ModelForm):
    class Meta:
        model = Qualification
        fields = '__all__'


class WorkExperienceForm(ModelForm):
    class Meta:
        model = WorkExperience
        fields = '__all__'
assword)
    if user is None:
        return HttpResponse('Incorrect creds')
    else:
        login(request, user)
        return HttpResponse('Login done')


def logout_route(request):
    logout(request)
    return HttpResponse('Done')


def requires_auth(request):
    if not request.user.is_authenticated:
        return redirect('{}?next={}'.format(reverse(login_view), request.path))
    else:
        return HttpResponse('You are authorized.')


@login_required
def test_authorized(request):
    return HttpResponse('Authorized success.')
