from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, reverse, render, get_object_or_404
from django.conf import settings
from django.forms.models import model_to_dict
import django.forms as forms

from . import models
from .models import UserProfile, Address, Qualification, WorkExperience

from .forms import User_SocialLinksForm, User_PersonalInfoForm, User_BasicInfoForm
from .forms import AddressForm, WorkExperienceForm, QualificationForm, WorkExperienceModelForm


def resolve_scope(request, username):
    allowed_scopes = [models.Visibility.public.value]
    if request.user.is_authenticated:
        allowed_scopes.append(models.Visibility.iiita.value)

    if request.user.username in ['admin', username]:
        allowed_scopes.append(models.Visibility.only_me.value)
    return allowed_scopes


# Create your views here.
def index(request):
    return render(request, 'index.html')


def demo(request):
    return render(request, 'demo.html')


def view_basic(request, username):
    user = get_object_or_404(User, username=username)
    profile = UserProfile.objects.get(user=user)
    context = {
        key: getattr(profile, key, None)
        for key in User_BasicInfoForm.Meta.fields
    }
    context['gender'] = str(models.Gender(context['gender']))
    context['username'] = user.username
    context['view_types'] = ['basic']
    return render(request, 'display_profile.html', context)


def view_social(request, username):
    user = get_object_or_404(User, username=username)
    profile = UserProfile.objects.get(user=user)
    context = {
        key: getattr(profile, key, None)
        for key in User_SocialLinksForm.Meta.fields
    }
    context['username'] = user.username
    context['view_types'] = ['social']

    return render(request, 'display_profile.html', context)


def view_personal(request, username):
    user = get_object_or_404(User, username=username)
    profile = UserProfile.objects.get(user=user)
    context = {
        key: getattr(profile, key, None)
        for key in User_PersonalInfoForm.Meta.fields
    }
    context['username'] = user.username
    context['permanent_address'] = profile.permanent_address
    context['current_address'] = profile.current_address
    context['view_types'] = ['misc']

    context['allowed_scopes'] = resolve_scope(request, username)
    return render(request, 'display_profile.html', context)


def view_work_experience(request, username):
    user = get_object_or_404(User, username=username)
    experiences = WorkExperience.objects.filter(user=user)
    return render(request, 'experience.html', context={'experiences': experiences})


@login_required
def update_basic(request, username):
    if username != request.user.username:
        return HttpResponse('Unauthorized', status=401)
    context = {
        'username': request.user.username,
        'form': None,
        'submit_url': reverse(update_basic, args=[username])
    }
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None

    if request.method == 'GET':
        if profile is None:
            context['form'] = User_BasicInfoForm()
        else:
            context['form'] = User_BasicInfoForm(initial=model_to_dict(profile))
        return render(request, 'generic_edit.html', context)
    else:
        if profile is None:
            form = User_BasicInfoForm(request.POST)
        else:
            form = User_BasicInfoForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect(reverse(view_basic, args=[context.get('username')]))
        else:
            context['form'] = form
            return render(request, 'generic_edit.html', context)


@login_required
def update_social(request, username):
    if username != request.user.username:
        return HttpResponse('Unauthorized', status=401)
    context = {
        'username': request.user.username,
        'form': None,
        'submit_url': reverse(update_social, args=[username])
    }
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None
    if request.method == 'GET':
        if profile is None:
            context['form'] = User_SocialLinksForm()
        else:
            context['form'] = User_SocialLinksForm(initial=model_to_dict(profile))
        return render(request, 'generic_edit.html', context)
    else:
        form = User_SocialLinksForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect(reverse(view_social, args=[context.get('username')]))
        else:
            context['form'] = form
            return render(request, 'generic_edit.html', context)


@login_required
def update_personal(request, username):
    if username != request.user.username:
        return HttpResponse('Unauthorized', status=401)
    context = {
        'username': request.user.username,
        'form': None,
        'submit_url': reverse(update_personal, args=[username])
    }
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None
    if request.method == 'GET':
        if profile is None:
            context['form'] = User_PersonalInfoForm()
        else:
            context['form'] = User_PersonalInfoForm(initial=model_to_dict(profile))
        return render(request, 'generic_edit.html', context)
    else:
        form = User_PersonalInfoForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect(reverse(view_misc, args=[context.get('username')]))
        else:
            context['form'] = form
            return render(request, 'generic_edit.html', context)


@login_required
def update_permanent_address(request, username):
    if username != request.user.username:
        return HttpResponse('Unauthorized', status=401)
    context = {
        'username': username,
        'form': None,
        'submit_url': reverse(update_permanent_address, args=[username])
    }
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        if profile.permanent_address is None:
            profile.permanent_address = Address.objects.create()
            profile.permanent_address.save()
            profile.save()
        form = AddressForm(request.POST, instance=profile.permanent_address)
        if form.is_valid():
            form.save()
            return redirect(view_misc, username=username)
        else:
            context['form'] = form
            return render(request, 'generic_edit.html', context)
    else:
        if profile.permanent_address is None:
            context['form'] = AddressForm()
        else:
            context['form'] = AddressForm(initial=model_to_dict(profile.permanent_address))
        return render(request, 'generic_edit.html', context)


@login_required
def update_current_address(request, username):
    if username != request.user.username:
        return HttpResponse('Unauthorized', status=401)
    context = {
        'username': username,
        'form': None,
        'submit_url': reverse(update_current_address, args=[username])
    }
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        if profile.current_address is None:
            profile.current_address = Address.objects.create()
            profile.current_address.save()
            profile.save()
        form = AddressForm(request.POST, instance=profile.current_address)
        if form.is_valid():
            form.save()
            return redirect(view_misc, username=username)
        else:
            context['form'] = form
            return render(request, 'generic_edit.html', context)
    else:
        if profile.current_address is None:
            context['form'] = AddressForm()
        else:
            context['form'] = AddressForm(initial=model_to_dict(profile.current_address))
        return render(request, 'generic_edit.html', context)



@login_required
def update_address(request, pk):
    try:
        address = Address.objects.get(pk=pk)
    except Address.DidNotFound:
        address = None
    else:
        if address.username != request.user.username:
            return HttpResponse('Unauthorized', status=401)

    context = {
        'form': None,
        'username': request.user.username,
        'submit_url': reverse(update_address, args=[pk])
    }

    if request.method == 'GET':
        if address is None:
            context['form'] = AddressForm()
        else:
            context['form'] = AddressForm(initial=model_to_dict(address))
        return render(request, 'generic_edit.html', context)
    else:
        form = None
        if address is None:
            form = AddressForm(request.POST)
        else:
            form = AddressForm(request.POST, instance=address)
        addr = form.save(commit=False)
        addr.username = request.user.username
        addr.save()
        return HttpResponse(addr.pk, status=200)


@login_required
def add_work_experience(request, username):
    if username != request.user.username:
        return HttpResponse('Unauthorized', status=401)

    context = {
        'username': username,
        'form': None,
        'submit_url': reverse(add_work_experience, args=[username])
    }
    if request.method == 'POST':
        form = WorkExperienceForm(request.POST)
        if form.is_valid():
            exp = WorkExperience(employer=request.POST.get('employer'),
                                 start_date=request.POST.get('start_date'),
                                 end_date=request.POST.get('end_date'),
                                 sector=request.POST.get('sector'),
                                 designation=request.POST.get('designation'),
                                 founder=True
                                 if request.POST.get('founder') is 'on' else False)
            exp.user = request.user
            exp.location = Address.objects.get(pk=request.POST.get('address_pk'))
            exp.save()
            return redirect(view_work_experience, username=username)
        else:
            context['form'] = form
            return render(request, 'generic_edit.html', context)
    else:
        context['form'] = WorkExperienceForm()
        return render(request, 'generic_edit.html', context)


@login_required
def delete_work_experience(request, username, pk):
    if username != request.user.username:
        return HttpResponse('Unauthorized', status=401)

    exp = get_object_or_404(WorkExperience, pk=pk)
    if exp.user.username != request.user.username:
        return HttpResponse('Unauthorized', status=401)

    exp.delete()
    return redirect(reverse(view_work_experience), args=[username])
