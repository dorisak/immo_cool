from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.template import loader
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from .forms import ConnectionForm
from .models import Administrator
from rental.models import Rental


def is_member(user):
    return user.groups.filter(name='Gestionnaires').exists()

# @user_passes_test(is_member)
@login_required
def home(request):
    """ Get the homepage and display the information for the dashboard """
    if request.method == 'GET':
        dash = []
        # admin_dashboard = Administrator.objects.filter(user__last_name='test')
        admin_dashboard = Administrator.objects.filter(user__email=request.user.email)
        context = {'admin_dash': admin_dashboard}

        template = loader.get_template('home/index.html')
        return HttpResponse(template.render(context, request))

def login_user(request):
    if request.method == 'POST':
        form = ConnectionForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    return render(request, 'login.html', {'form': form})
            else:
                messages.error(request, 'informations erronées')
    else:
        form = ConnectionForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    """  Logout the user """
    logout(request)
    messages.success(request, 'Vous êtes déconnecté')
    return redirect('home:login')
