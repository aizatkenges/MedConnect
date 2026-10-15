from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "appointment",
        "get_doctor",
        "get_patient",
        "rating",
        "created_at",
    )
    list_display_links = ("id", "appointment")
    list_filter = ("rating", "created_at", "appointment__doctor")
    search_fields = (
        "comment",
        "appointment__patient__email",
        "appointment__doctor__user__email",
    )
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    readonly_fields = ("created_at",)
    raw_id_fields = ("appointment",)
    list_per_page = 25
    actions = ["delete_low_rated"]

    def get_queryset(self, request: HttpRequest) -> QuerySet[Review]:
        return (
            super()
            .get_queryset(request)
            .select_related("appointment__patient", "appointment__doctor__user")
        )

    @admin.display(description="Doctor", ordering="appointment__doctor")
    def get_doctor(self, obj: Review) -> str:
        return str(obj.appointment.doctor)

    @admin.display(description="Patient", ordering="appointment__patient")
    def get_patient(self, obj: Review) -> str:
        return str(obj.appointment.patient)

    @admin.action(description="Delete reviews with rating 1")
    def delete_low_rated(
        self, request: HttpRequest, queryset: QuerySet[Review]
    ) -> None:
        queryset.filter(rating=1).delete()
