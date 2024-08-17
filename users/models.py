from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    a_class = models.IntegerField(null=True, blank=True)


class TrainCruise(models.Model):
    train_number = models.CharField(max_length=20, null=True, blank=True)
    departure_station = models.CharField(max_length=100, null=True, blank=True)
    arrival_station = models.CharField(max_length=100, null=True, blank=True)
    departure_time = models.DateTimeField(null=True, blank=True)
    arrival_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.train_number} - {self.departure_station} to {self.arrival_station}"



class TrainTicket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    train = models.ForeignKey(TrainCruise, on_delete=models.CASCADE, related_name='train', null=True, blank=True)
    seat_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.train}"


class BiometricProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    face_data = models.BinaryField()  # Сохранение бинарных данных для фото

    def __str__(self):
        return f"{self.user.username}"


class RobotProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    now_cruise = models.OneToOneField(TrainCruise, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.now_cruise.train_number}"

