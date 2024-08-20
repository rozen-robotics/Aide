from django.db import models
from django.contrib.auth.models import AbstractUser

class TrainInfo(models.Model):
    train_number = models.CharField(max_length=20)
    departure_station = models.CharField(max_length=100)
    arrival_station = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    def __str__(self):
        return f"Train {self.train_number}: {self.departure_station} to {self.arrival_station}"


class TrainTicket(models.Model):
    user_id = models.IntegerField(null=True, blank=True)
    user_name = models.CharField(max_length=50, null=True, blank=True)
    face_data = models.BinaryField(null=True, blank=True)
    seat_number = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name} - {self.seat_number}"


