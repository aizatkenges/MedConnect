from django.contrib import admin, messages
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'patient',
        'doctor',
        'date',
        'time',
        'status',
        'created_at',
    )
    list_display_links = ('id', 'patient')
    list_filter = ('status', 'date', 'doctor')
    search_fields = (
        'patient__email',
        'patient__first_name',
        'patient__last_name',
        'doctor__user__first_name',
        'doctor__user__last_name',
        'reason',
    )
    list_select_related = ('patient', 'doctor')
    list_editable = ('status',)
    date_hierarchy = 'date'
    ordering = ('-date', '-time')
    readonly_fields = ('created_at',)
    actions = ('mark_confirmed', 'mark_completed', 'mark_cancelled')

    fieldsets = (
        ('Participants', {'fields': ('patient', 'doctor')}),
        ('Schedule', {'fields': ('date', 'time')}),
        ('Details', {'fields': ('reason', 'status', 'created_at')}),
    )

    @admin.action(description='Mark selected as confirmed')
    def mark_confirmed(self, request: HttpRequest, queryset: QuerySet) -> None:
        updated = queryset.update(status=Appointment.Status.CONFIRMED)
        self.message_user(request, f'{updated} confirmed.', messages.SUCCESS)

    @admin.action(description='Mark selected as completed')
    def mark_completed(self, request: HttpRequest, queryset: QuerySet) -> None:
        updated = queryset.update(status=Appointment.Status.COMPLETED)
        self.message_user(request, f'{updated} completed.', messages.SUCCESS)

    @admin.action(description='Mark selected as cancelled')
    def mark_cancelled(self, request: HttpRequest, queryset: QuerySet) -> None:
        updated = queryset.update(status=Appointment.Status.CANCELLED)
        self.message_user(request, f'{updated} cancelled.', messages.SUCCESS)
        