from django.contrib import admin

from .models import Doctor, Patient, PatientDoctorMapping


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "age",
        "gender",
        "phone",
        "owner",
        "created_at",
    )
    search_fields = ("name", "phone")
    list_filter = ("gender",)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "specialization",
        "email",
        "phone",
    )
    search_fields = (
        "name",
        "specialization",
        "email",
    )


@admin.register(PatientDoctorMapping)
class MappingAdmin(admin.ModelAdmin):
    list_display = (
        "patient",
        "doctor",
        "assigned_at",
    )
    search_fields = (
        "patient__name",
        "doctor__name",
    )
