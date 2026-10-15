import datetime

from django.db import IntegrityError, transaction
from django.test import TestCase

from apps.doctor.models import DoctorProfile, Specialization
from apps.users.models import User

from .models import Appointment


class AppointmentTests(TestCase):
    def setUp(self) -> None:
        self.patient = User.objects.create_user(
            email='p@test.kz', password='pass12345', role='patient'
        )
        doc_user = User.objects.create_user(
            email='d@test.kz', password='pass12345', role='doctor'
        )
        self.doctor = DoctorProfile.objects.create(
            user=doc_user,
            specialization=Specialization.objects.create(name='Cardiology'),
            license_number='LIC-001',
            experience_years=5,
            consultation_price=100,
        )

    def _make(self, **kwargs) -> Appointment:
        data = dict(
            patient=self.patient,
            doctor=self.doctor,
            date=datetime.date(2026, 11, 1),
            time=datetime.time(10, 0),
            reason='Checkup',
        )
        data.update(kwargs)
        return Appointment.objects.create(**data)

    def test_default_status_is_pending(self) -> None:
        self.assertEqual(self._make().status, Appointment.Status.PENDING)

    def test_status_transitions(self) -> None:
        appt = self._make()
        appt.confirm()
        self.assertEqual(appt.status, 'confirmed')
        appt.complete()
        self.assertEqual(appt.status, 'completed')

    def test_double_booking_blocked(self) -> None:
        self._make()
        with self.assertRaises(IntegrityError), transaction.atomic():
            self._make()

    def test_slot_free_after_cancel(self) -> None:
        self._make().cancel()
        self._make()