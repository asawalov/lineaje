from django.db import models
from datetime import datetime

# class User(models.Model):
#     vehicle_type = models.CharField(max_length=50)
#     license_plate = models.CharField(max_length=50, unique=True)


class Rate(models.Model):
    spot_type = models.CharField(unique=True)  # 2 wheeler or 4 wheeler
    rate_per_hour = models.FloatField()


class ParkingLot(models.Model):
    name = models.CharField(max_length=100, unique=True)
    total_floors = models.IntegerField()
    total_spots = models.IntegerField()


class Floor(models.Model):
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE)
    floor_number = models.IntegerField()
    total_2_wheeler_spots = models.IntegerField()
    total_4_wheeler_spots = models.IntegerField()

    class Meta:
        unique_together = ('parking_lot', 'floor_number')


class ParkingSpot(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    spot_type = models.CharField(max_length=50)  # 2 wheeler or 4 wheeler
    is_occupied = models.BooleanField(default=False)


class ParkingSession(models.Model):
    license_plate = models.CharField(max_length=50)
    parking_spot = models.ForeignKey(ParkingSpot, on_delete=models.SET_NULL, null=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ('license_plate', 'parking_spot', 'start_time')
