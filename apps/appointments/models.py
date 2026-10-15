from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q


class Appointment(models.Model):

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointments',
    )
    doctor = models.ForeignKey(
        'doctors.DoctorProfile',
        on_delete=models.CASCADE,
        related_name='appointments',
    )
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-time']
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'date', 'time'],
                condition=~Q(status='cancelled'),
                name='unique_active_doctor_slot',
            ),
        ]

    def __str__(self) -> str:
        return f'Appointment {self.id}: {self.date} {self.time} ({self.status})'

    def clean(self) -> None:
        super().clean()
        if self.patient_id and getattr(self.patient, 'role', 'patient') != 'patient':
            raise ValidationError({'patient': 'Selected user is not a patient.'})

    @property
    def is_active(self) -> bool:
        return self.status in (self.Status.PENDING, self.Status.CONFIRMED)

    def confirm(self) -> None:
        self.status = self.Status.CONFIRMED
        self.save(update_fields=['status'])

    def complete(self) -> None:
        self.status = self.Status.COMPLETED
        self.save(update_fields=['status'])

    def cancel(self) -> None:
        self.status = self.Status.CANCELLED
        self.save(update_fields=['status'])