from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.db import models



    
class User(AbstractUser):
    ROLE_CHOICES = [
        ('client', 'Client'),
        ('specialist', 'Specialist'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')
    phone = models.CharField(max_length=20, blank=True, default="")
    email= models.CharField(max_length=40, blank=True, default="")
    services = models.ManyToManyField('Service', blank=True, related_name='specialists') 
    work_start_time = models.TimeField(null = True, blank = True)
    work_end_time = models.TimeField(null = True, blank = True)



    def save(self, *args, **kwargs):
        if self.role == 'client':
            self.work_start_time = None
            self.work_end_time = None
        super().save(*args, **kwargs)
        

    def __str__(self):
        return f"{self.username} ({self.role})"




class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title





class Booking(models.Model):
    SERVICE_CHOICES =(
        ('upcoming', 'Upcoming'),
        ('canceled', 'Canceled'),
        ('completed', 'Completed'),
)
    service_choices = models.CharField(max_length=20, choices=SERVICE_CHOICES, default='upcoming')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    client = models.ForeignKey(
        User, on_delete=models.CASCADE,
        limit_choices_to={'role': 'client'},
        related_name='appointments_as_client'
    )
    specialist = models.ForeignKey(
        User, on_delete=models.CASCADE,
        limit_choices_to={'role': 'specialist'},
        related_name='appointments_as_specialist'
    )
    date = models.DateField()
    time = models.TimeField()
    created_dt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service}: {self.client} to {self.specialist} on {self.date} in {self.time}"
    




class Message(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='message')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_dt = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'New message from {self.sender} {self.created_dt.strftime("%Y-%m-%d %H:%M")}'
    



