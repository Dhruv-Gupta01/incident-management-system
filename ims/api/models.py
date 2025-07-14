from django.db import models
from django.contrib.auth.models import User
import random
import datetime

# 📦 User Profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to default Django User
    phone = models.CharField(max_length=15)
    address = models.TextField()
    pin_code = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username

# 🔥 Incident model
def generate_incident_id():
    return f"RMG{random.randint(10000, 99999)}{datetime.datetime.now().year}"

class Incident(models.Model):
    INCIDENT_STATUS = [
        ('Open', 'Open'),
        ('In progress', 'In progress'),
        ('Closed', 'Closed'),
    ]
    PRIORITY = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]

    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    incident_id = models.CharField(max_length=20, unique=True, default=generate_incident_id)
    is_enterprise = models.BooleanField()
    reporter_name = models.CharField(max_length=100)
    details = models.TextField()
    reported_on = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=10, choices=PRIORITY)
    status = models.CharField(max_length=20, choices=INCIDENT_STATUS)

    def __str__(self):
        return self.incident_id
