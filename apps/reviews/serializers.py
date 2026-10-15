from rest_framework import serializers

from apps.appointments.models import Appointment
from apps.users.models import User

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    doctor = serializers.IntegerField(
        source="appointment.doctor_id", read_only=True
    )

    class Meta:
        model = Review
        fields = [
            "id",
            "appointment",
            "doctor",
            "rating",
            "comment",
            "created_at",
        ]
        read_only_fields = ["id", "doctor", "created_at"]

    def validate_appointment(self, appointment: Appointment) -> Appointment:
        user: User = self.context["request"].user

        if self.instance is not None:
            if appointment != self.instance.appointment:
                raise serializers.ValidationError(
                    "Appointment cannot be changed."
                )
            return appointment

        if appointment.patient_id != user.pk:
            raise serializers.ValidationError(
                "You can review only your own appointment."
            )
        if appointment.status != Appointment.status.COMPLETED:
            raise serializers.ValidationError(
                "You can review only a completed appointment."
            )
        if Review.objects.filter(appointment=appointment).exists():
            raise serializers.ValidationError(
                "This appointment already has a review."
            )
        return appointment
