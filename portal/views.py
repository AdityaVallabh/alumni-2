from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, reverse, render, get_object_or_404
from django.conf import settings
from django.forms.models import model_to_dict
import django.forms as forms

from .models import UserProfile, Address, Qualification, WorkExperience

from .forms import User_SocialLinksForm, User_MiscInfoForm, User_BasicInfoForm


# Create your views here.
def view_basic(request, username):
    user = get_object_or_404(User, username=username)
    profile = UserProfile.objects.get(user=user)
    context = {
        key: getattr(profile, key, None)
        for key in User_BasicInfoForm.Meta.fields
    }
    context['username'] = user.username
    return render(request, 'generic_display.html', context)


def view_social(request, username):
    user = get_object_or_404(User, username=username)
    profile = UserProfile.objects.get(user=user)
    context = {
        key: getattr(profile, key, None)
        for key in User_SocialLinksForm.Meta.fields
    }
    context['username'] = user.username
    return render(request, 'generic_display.html', context)


def view_misc(request, username):
    user = get_object_or_404(User, username=username)
    profile = UserProfile.objects.get(user=user)
    context = {
        key: getattr(profile, key, None)
        for key in User_MiscInfoForm.Meta.fields
    }
    context['username'] = user.username
    return render(request, 'generic_display.html', context)

def view_work_experience(request, username):
    user = get_object_or_404(User, username=username)
    experiences = WorkExperience.objects.get(user=user)

    context = {
        key: getattr(experiences, key, None)
        for key in WorkExperienceForm.Meta.fields
    }

    context['work_experience'] = experiences
    return render(request, 'generic_display.html', context)

@login_required
def update_basic(request):
    context = {
        'username': request.user.username,
        'form': None,
        'submit_url': reverse(update_basic)
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
def update_social(request):
    context = {
        'username': request.user.username,
        'form': None,
        'submit_url': reverse(update_social)
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
def update_misc(request):
    context = {
        'username': request.user.username,
        'form': None,
        'submit_url': reverse(update_basic)
    }
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None
    if request.method == 'GET':
        if profile is None:
            context['form'] = User_MiscInfoForm()
        else:
            context['form'] = User_MiscInfoForm(initial=model_to_dict(profile))
        return render(request, 'generic_edit.html', context)
    else:
        form = User_MiscInfoForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            context['form'] = form
            return render(request, 'generic_edit.html', context)

@login_required
def update_work_experience(request):
    return render(request, 'generic_edit.html', context)
