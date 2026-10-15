from django.db import models

from django.db import models


class Specialization(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    def __str__(self) -> str:
        return self.name


class DoctorProfile(models.Model):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )

    specialization = models.ForeignKey(
        Specialization,
        on_delete=models.CASCADE,
    )

    license_number = models.CharField(
        max_length=100,
        unique=True,
    )

    experience_years = models.PositiveIntegerField()

    bio = models.TextField(
        blank=True,
    )

    consultation_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"


class DoctorSchedule(models.Model):
    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.CASCADE,
    )

    day_of_week = models.CharField(
        max_length=20,
    )

    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self) -> str:
        return f"{self.doctor} - {self.day_of_week}"