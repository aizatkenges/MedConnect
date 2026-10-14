from django.contrib import admin
from .models import Prescription, Medication


class PrescriptionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "appointment",
        "created_at",
    )
    search_fields = (
        "diagnosis",
    )

class MedicalAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "prescription",
        "dosage",
        "frequency",
        "duration_days",
    )

    search_fields = (
        "name",
    )


admin.site.register(Prescription, PrescriptionAdmin)

admin.site.register(Medication, MedicalAdmin)