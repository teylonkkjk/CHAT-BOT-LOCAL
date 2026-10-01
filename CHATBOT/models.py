from django.db import models

class Message(models.Model):
    ROLE_CHOICES = (
        ('user', 'Usuário'),
        ('assistant', 'Assistente'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['timestamp']