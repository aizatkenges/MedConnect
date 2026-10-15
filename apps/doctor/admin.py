from django.contrib import admin
from .models import DoctorProfile, DoctorSchedule, Specialization


class SpecializationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )

    search_fields = (
        "name",
    )


class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "specialization",
        "license_number",
        "experience_years",
        "consultation_price",
    )

    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
        "license_number",
    )

    list_filter = (
        "specialization",
    )


class DoctorScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "doctor",
        "day_of_week",
        "start_time",
        "end_time",
    )

    list_filter = (
        "day_of_week",
    )


admin.site.register(Specialization, SpecializationAdmin)
admin.site.register(DoctorProfile, DoctorProfileAdmin)
admin.site.register(DoctorSchedule, DoctorScheduleAdmin)
