from rest_framework import serializers

from .models import Doctor, Patient, PatientDoctorMapping

# Converts patient model data into JSON and validates incoming patient data.

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "id",
            "name",
            "age",
            "gender",
            "address",
            "phone",
            "medical_history",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Name is required.")

        return value

    def validate_age(self, value):
        if value > 120:
            raise serializers.ValidationError("Please enter a valid age.")

        return value

    def validate_phone(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Phone number is required.")

        return value

# Handles doctor data received from and sent to the API.

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [
            "id",
            "name",
            "specialization",
            "email",
            "phone",
            "experience_years",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Name is required.")

        return value

    def validate_specialization(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Specialization is required."
            )

        return value

    def validate_email(self, value):
        return value.lower().strip()

    def validate_experience_years(self, value):
        if value > 80:
            raise serializers.ValidationError(
                "Please enter a valid experience value."
            )

        return value

# Handles the relationship between a patient and a doctor.

class MappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDoctorMapping
        fields = [
            "id",
            "patient",
            "doctor",
            "assigned_at",
        ]
        read_only_fields = ["id", "assigned_at"]

    def validate(self, attrs):
        patient = attrs["patient"]
        doctor = attrs["doctor"]
        request = self.context.get("request")

        # A user must own the patient before they can assign a doctor to it.
        if request and patient.owner_id != request.user.id:
            raise serializers.ValidationError(
                {
                    "patient": (
                        "You can only assign doctors to your own patients."
                    )
                }
            )

        if PatientDoctorMapping.objects.filter(
            patient=patient,
            doctor=doctor,
        ).exists():
            raise serializers.ValidationError(
                {
                    "doctor": (
                        "This doctor is already assigned to the patient."
                    )
                }
            )

        return attrs
