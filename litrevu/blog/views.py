from itertools import chain
from django.db.models import CharField, Value
from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import *
from authentication.forms import CustomAuthenticationForm
from django.views.generic.edit import  CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import Http404
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib import messages
from django import forms

User = get_user_model()


@never_cache
def home(request):    
    form = CustomAuthenticationForm()

    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user is not None:
                login(request, user) 
                return redirect('dashboard')
           

    return render(request, 'blog/home.html', {'form': form})




@login_required
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

    for post in posts:
        if post.type == 'review':
            if post.rating is not None:
                post.full_stars = range(post.rating)
                post.empty_stars = range(5 - post.rating)
            else:
                post.full_stars = range(0)
                post.empty_stars = range(5)
    
    return render(request, 'blog/dashboard.html', {'posts': posts})

@login_required
def user_posts(request):
    user_tickets = Ticket.objects.filter(user=request.user).annotate(type=Value('ticket', output_field=CharField()))
    user_reviews = Review.objects.filter(user=request.user).annotate(type=Value('review', output_field=CharField()))

    user_posts = sorted(
        chain(user_tickets, user_reviews),
        key=lambda post : post.created_at,
        reverse=True
    ) 

    for post in user_posts:
        if post.type == 'review':
            if post.rating is not None:
                post.full_stars = range(post.rating)
                post.empty_stars = range(5 - post.rating)
        else:
                post.full_stars = range(0)
                post.empty_stars = range(5)
    return render(request, 'blog/user_posts.html', {'user_posts': user_posts})

        

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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket_id = self.kwargs.get("ticket_id")
        context['ticket'] = get_object_or_404(Ticket, id=ticket_id)
        return context
    
    def get_success_url(self):
        return '/dashboard/'



class ReviewWithoutTicket(CreateView):
    model = Review
    template_name = 'blog/review_without_ticket.html'
    fields = ['title', 'description', 'image', 'review_title','rating', 'content']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['rating'].widget = forms.RadioSelect(choices=[
            (0, '0'),
            (1, '1'),
            (2, '2'),
            (3, '3'),
            (4, '4'),
            (5, '5')
        ])
        return form
    
    def form_valid(self, form):
        form.instance.user = self.request.user
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

    

class ReviewUpdate(UpdateView):
    model = Review
    template_name = 'blog/review_form.html'
    fields = ['review_title', 'content', 'rating', 'image']

    def get_queryset(self):
        queryset = Review.objects.filter(user=self.request.user)
        print("Critiques accessibles :", queryset)
        return queryset
    
    def get_success_url(self):
        return reverse_lazy('dashboard')
    

class PostDelete(DeleteView):    
    template_name = 'blog/post_delete.html'

    def get_object(self, queryset=None):
        model = self.kwargs.get('model')
        pk = self.kwargs.get("pk")
        if model == 'ticket':
            return get_object_or_404(Ticket, pk=pk)
        elif model == 'review':
            return get_object_or_404(Review, pk=pk)
        else:
            return Http404('objet non trouvé')

        
    def get_success_url(self):
        return reverse_lazy('dashboard')
    

@login_required
def manage_follows(request):
    if request.method == 'POST':
        followed_username = request.POST.get('followed_username')
        followed_user = get_object_or_404(User, username=followed_username)

        if followed_user == request.user:
            messages.warning(request, f'Vous suivez déja {followed_user.username}')
            return redirect('manage_follows')
        
        UserFollows.objects.create(follower=request.user, followed=followed_user)
        messages.success(request, f'Vous suivez maintenant {followed_user.username}')
        return redirect('manage_follows')
    following = UserFollows.objects.filter(follower=request.user)
    followers = UserFollows.objects.filter(followed=request.user)

    return render(request, 'blog/manage_follows.html', {'following': following, 'followers': followers})

@login_required
def unfollow(request,  user_id):
    followed_user = get_object_or_404(User, id=user_id)
    follow = UserFollows.objects.filter(follower=request.user, followed=followed_user).first()

    if follow:
        follow.delete()
        messages.success(request, f'Vous vous êtes désabonné de {followed_user.username}')
    
    return redirect('manage_follows')


    



