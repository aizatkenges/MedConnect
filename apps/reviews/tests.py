from datetime import time, timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.appointments.models import Appointment, AppointmentStatus
from apps.doctor.models import DoctorProfile, Specialization
from apps.users.models import Role, User

from .models import Review


class ReviewAPITests(APITestCase):
    def setUp(self) -> None:
        self.patient = User.objects.create_user(
            "p@test.kz", "pass12345", first_name="P", last_name="T",
            role=Role.PATIENT,
        )
        self.other = User.objects.create_user(
            "o@test.kz", "pass12345", first_name="O", last_name="T",
            role=Role.PATIENT,
        )
        doctor_user = User.objects.create_user(
            "d@test.kz", "pass12345", first_name="D", last_name="T",
            role=Role.DOCTOR,
        )
        spec = Specialization.objects.create(name="Cardiology")
        doctor = DoctorProfile.objects.create(
            user=doctor_user, specialization=spec,
            license_number="L-1", experience_years=5,
        )
        self.appointment = Appointment.objects.create(
            patient=self.patient, doctor=doctor,
            date=timezone.localdate() - timedelta(days=1),
            time=time(10, 0), reason="checkup",
            status=AppointmentStatus.COMPLETED,
        )
        self.url = reverse("review-list")

    def test_patient_can_create_review(self) -> None:
        self.client.force_authenticate(self.patient)
        response = self.client.post(
            self.url, {"appointment": self.appointment.pk, "rating": 5}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_other_user_cannot_review(self) -> None:
        self.client.force_authenticate(self.other)
        response = self.client.post(
            self.url, {"appointment": self.appointment.pk, "rating": 5}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rating_out_of_range(self) -> None:
        self.client.force_authenticate(self.patient)
        response = self.client.post(
            self.url, {"appointment": self.appointment.pk, "rating": 6}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_review_rejected(self) -> None:
        Review.objects.create(appointment=self.appointment, rating=4)
        self.client.force_authenticate(self.patient)
        response = self.client.post(
            self.url, {"appointment": self.appointment.pk, "rating": 5}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
