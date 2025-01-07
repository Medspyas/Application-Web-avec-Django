"""
URL configuration for litrevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView)
from django.urls import path
from blog.views import home , dashboard, user_posts ,TicketCreateView, ReviewWithTicket, ReviewWithoutTicket, TicketUpdate, PostDelete, ReviewUpdate, manage_follows, unfollow
from authentication.views import signup_page


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),   
    path('logout', LogoutView.as_view(), name='logout'),
    path('signup/', signup_page, name='signup'),
    path('dashboard/', dashboard, name='dashboard' ),
    path('posts/', user_posts, name='user_posts'),
    path('request-ticket/', TicketCreateView.as_view(), name = 'request_ticket'),
    path('review/ticket/<int:ticket_id>/', ReviewWithTicket.as_view(), name='review_with_ticket'),
    path('review/create/', ReviewWithoutTicket.as_view(), name='review_without_ticket'),
    path('ticket/<int:pk>/edit/', TicketUpdate.as_view(), name='ticket_edit'), 
    path('review/<int:pk>/edit/', ReviewUpdate.as_view(), name='review_edit'),
    path('<str:model>/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'), 
    path('follows/', manage_follows, name= 'manage_follows'),
    path('unfollow/<int:user_id>/', unfollow, name= 'unfollow'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
