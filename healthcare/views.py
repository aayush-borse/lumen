from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins

from .models import Doctor, Patient, PatientDoctorMapping
from .serializers import DoctorSerializer, MappingSerializer, PatientSerializer

# Returns the current user's patients or creates a new patient.

class PatientListCreateView(generics.ListCreateAPIView):
    serializer_class = PatientSerializer

    def get_queryset(self):
        # Patients are private to the user who created them.
        return Patient.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# Handles viewing, updating and deleting a single patient.

class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PatientSerializer

# Only return patients belonging to the currently logged-in user.
# This prevents users from accessing another user's patient records.
    def get_queryset(self):
        # This also prevents one user from changing another user's patient.
        return Patient.objects.filter(owner=self.request.user)

# Returns all doctors or creates a new doctor.

class DoctorListCreateView(generics.ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

# Handles viewing, updating and deleting a single doctor.

class DoctorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

# Creates a patient-doctor mapping and lists existing mappings.

class MappingListCreateView(generics.ListCreateAPIView):
    serializer_class = MappingSerializer

    def get_queryset(self):
        # Only mappings belonging to the logged-in user's patients are shown.
        return PatientDoctorMapping.objects.filter(
            patient__owner=self.request.user
        ).select_related("patient", "doctor")

# Returns all doctors assigned to a particular patient.
# DELETE uses the same URL pattern to remove a mapping by its ID.

class MappingByPatientView(
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    """
    The assignment uses the same URL pattern for two different operations:

    GET    /api/mappings/<patient_id>/ -> mappings for that patient
    DELETE /api/mappings/<id>/         -> delete that mapping

    HTTP methods make the two operations distinguishable.
    """

    serializer_class = MappingSerializer

    def get_queryset(self):
        if self.request.method == "GET":
            patient_id = self.kwargs["pk"]

            # Make sure the requested patient belongs to this user.
            get_object_or_404(
                Patient,
                id=patient_id,
                owner=self.request.user,
            )

            return PatientDoctorMapping.objects.filter(
                patient_id=patient_id
            ).select_related("patient", "doctor")

        # DELETE can only remove mappings for the user's own patients.
        return PatientDoctorMapping.objects.filter(
            patient__owner=self.request.user
        )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
