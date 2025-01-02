from itertools import chain
from django.db.models import CharField, Value
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import *
from django.views.generic.edit import  CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy



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

class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    template_name = 'blog/request_ticket.html'
    fields = ['title', 'description', 'image']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    

    def get_success_url(self):
        return '/dashboard/'
    
class ReviewWithTicket(CreateView):
    model = Review
    template_name = 'blog/review_with_ticket.html'
    fields = ['review_title', 'rating', 'content']

    def form_valid(self, form):
        form.instance.user = self.request.user

        ticket_id = self.kwargs.get("ticket_id")
        form.instance.ticket = get_object_or_404(Ticket, id=ticket_id)
        return super().form_valid(form)
    
    def get_success_url(self):
        return '/dashboard/'



class ReviewWithoutTicket(CreateView):
    model = Review
    template_name = 'blog/review_without_ticket.html'
    fields = ['title', 'description', 'image', 'review_title','rating', 'content']

    def form_valid(self, form):
        form.instance.user = self.requests.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return '/dashboard/'
    
class TicketUpdate(UpdateView):
    model = Ticket
    template_name = 'blog/ticket_form.html'
    fields = ['title', 'description', 'image']

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('dashboard')
    
class TicketDelete(DeleteView):
    model = Ticket
    template_name = 'blog/ticket_delete.html'

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user) 
    
    def get_success_url(self):
        return reverse_lazy('dashboard')
    



