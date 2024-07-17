from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .forms import SignUpForm, ProfileUpdateForm, UserUpdateForm, LoginForm
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.views.generic import DetailView
import logging
from django.urls import reverse_lazy

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()
            profile_img = form.cleaned_data.get('profile_img')

            if profile_img:
                profile = user.profile
                profile.profile_img = profile_img
                profile.save()
            
            messages.success(request, f'Account created for {user.username}!')

            login(request, user)
            return redirect('main:home_loggedin')

    else:
        form = SignUpForm()

    return render(request, 'user/signup.html', {
                            'form': form
                            })

logger = logging.getLogger(__name__)
class CustomLoginView(LoginView):
    template_name = 'user/login.html'
    authentication_form = LoginForm

    def form_valid(self, form):
        try: 
            response = super().form_valid(form)

            user = form.get_user()
            logger.info('User %s logged in', user.username)
            messages.success(self.request, f'Welcome back {user.username}!')

            return response
        except Exception as e:
            logger.error(e)
            return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('main:home_loggedin')

@login_required
def profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user_profile)
    profile_img = profile.profile_img.url
    profile_bio = profile.bio
    # add user events here + categories
    # user_items = Item.objects.filter(created_by=user_profile, is_sold=False)[:6]

    return render(request, 'user/profile.html', {
        'profile_img': profile_img,
        'profile_bio': profile_bio,
        'current_user': request.user,
        'user_profile': user_profile,
        'profile': profile,
    })

@login_required
def profile_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('user:profile', username=request.user.username)

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'user/profile_update.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

class UserProfileView(DetailView):
    model = User
    template_name = 'user/profile.html'
    context_object_name = 'user_profile'

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs['username'])