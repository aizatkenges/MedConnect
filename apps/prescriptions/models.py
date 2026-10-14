from django.db import models
from django.conf import settings

#1 appointment - 1 prescription
class Prescription(models.Model):
    appointment = models.OneToOneField("appointments.Appointment", on_delete=models.CASCADE)
    diagnosis = models.TextField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'Prescription {self.id}'


#1 prescription - N Medications
class Medication(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete = models.CASCADE)
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    duration_days = models.IntegerField()
    instructions = models.TextField(blank=True)

    def __str__(self)->str:
        return self.name

