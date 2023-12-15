from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, View
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Profile
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm


# Create your views here.
@login_required
def dashboard_view(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    context = {
        'user':user,
        'profile':profile

    }
    return render(request, 'pages/user_profile.html', context)





# class SignUpView(CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy('login')  # Redirect to the login page upon successful registration
#     template_name = 'account/register.html'  # Replace with the path to your signup template


def user_register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            Profile.objects.create(user=new_user)
            context = {
                'new_user':new_user
            }
            return render(request, 'account/register_done.html', context)
    else:
        user_form  = UserRegistrationForm()
        success_url = reverse_lazy('login')
        context = {
            'user_form':user_form
        }
        return render(request, 'account/register.html', {'user_form': user_form})
    
@login_required
def edit_user(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        success_url = reverse_lazy('user_profile')
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')
        
        else:
            user_form = UserEditForm(instance=request.user)
            profile_form = ProfileEditForm(instance=request.user.profile)

        return render(request, 'account/profile_edit.html', {"user_form":user_form,"profile_form":profile_form})
    

class EditUserView(LoginRequiredMixin, View):
    def get(self, request):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request, 'account/profile_edit.html',{"user_form":user_form,"profile_form":profile_form})

    def post(self, request):
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')

        