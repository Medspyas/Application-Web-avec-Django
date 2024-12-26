from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache


@never_cache
def home(request):    
    form = AuthenticationForm()
    return render(request, 'blog/home.html', {'form': form})

@login_required
def connected(request):
    return render(request, 'blog/connected.html')







