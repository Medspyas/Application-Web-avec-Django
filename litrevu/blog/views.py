from itertools import chain
from django.db.models import CharField, Value
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import *


@never_cache
def home(request):    
    form = AuthenticationForm()
    return render(request, 'blog/home.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'blog/dashboard.html')


def dashboard(request):
    tickets = Ticket.objects.all()    
    reviews = Review.objects.all()
    

    tickets =tickets.annotate(type=Value('ticket', output_field=CharField()))
    reviews = reviews.annotate(type=Value('review', output_field=CharField()))

    posts = sorted(
        chain(tickets, reviews), 
        key=lambda post : post.created_at,
        reverse=True
    )
    print("Tickets :", tickets)
    print("Reviews :", reviews)
    print("Posts :", posts)
   
    return render(request, 'blog/dashboard.html', {'posts': posts})






