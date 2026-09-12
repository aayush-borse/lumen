from django.urls import path

from .views import (
    DoctorDetailView,
    DoctorListCreateView,
    MappingByPatientView,
    MappingListCreateView,
    PatientDetailView,
    PatientListCreateView,
)

# API routes for patients, doctors and patient-doctor mappings.

urlpatterns = [
    # Patient endpoints
    path(
        "patients/",
        PatientListCreateView.as_view(),
        name="patient-list",
    ),
    path(
        "patients/<int:pk>/",
        PatientDetailView.as_view(),
        name="patient-detail",
    ),
 
# Doctor endpoints
    path(
        "doctors/",
        DoctorListCreateView.as_view(),
        name="doctor-list",
    ),
    path(
        "doctors/<int:pk>/",
        DoctorDetailView.as_view(),
        name="doctor-detail",
    ),

# Mapping endpoints
    path(
        "mappings/",
        MappingListCreateView.as_view(),
        name="mapping-list",
    ),
    path(
        "mappings/<int:pk>/",
        MappingByPatientView.as_view(),
        name="mapping-by-patient-or-delete",
    ),
]
