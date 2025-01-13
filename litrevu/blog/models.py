from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator , MinValueValidator
from django.urls import reverse


class Ticket(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, blank=True, null=True)
    image = models.ImageField(upload_to='tickets/', blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class UserFollows(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following'
    )

    followed = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='followers'
        )
    
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')
        verbose_name = 'Relation de suivi'
        verbose_name_plural = 'Relation de suivi'

    def __str__(self):
        return f'{self.follower.username} suit {self.followed.username}'
    
class Review(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ticket = models.ForeignKey(
        'Ticket',
        on_delete=models.CASCADE,
        null=True, 
        blank=True,
        related_name='reviews'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, blank=True, null=True)
    image = models.ImageField(upload_to='reviews/', blank=True, null=True)

    review_title = models.CharField(max_length=200)
    content = models.TextField(max_length=2000)
    
    rating = models.IntegerField(
        null=True, blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('dashboard')

    def __str__(self):
        if self.ticket:
            return f'Critique de {self.user.username} sur {self.ticket.title}'
        return f'Critique de {self.user.username}'