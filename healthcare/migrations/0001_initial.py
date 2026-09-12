from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Doctor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "specialization",
                    models.CharField(max_length=100),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=254,
                        unique=True,
                    ),
                ),
                ("phone", models.CharField(max_length=20)),
                (
                    "experience_years",
                    models.PositiveIntegerField(default=0),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True),
                ),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Patient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("age", models.PositiveIntegerField()),
                ("gender", models.CharField(max_length=20)),
                ("address", models.TextField()),
                ("phone", models.CharField(max_length=20)),
                (
                    "medical_history",
                    models.TextField(blank=True),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="patients",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="PatientDoctorMapping",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "assigned_at",
                    models.DateTimeField(auto_now_add=True),
                ),
                (
                    "doctor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="patient_mappings",
                        to="healthcare.doctor",
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="doctor_mappings",
                        to="healthcare.patient",
                    ),
                ),
            ],
            options={
                "ordering": ["-assigned_at"],
            },
        ),
        migrations.AddConstraint(
            model_name="patientdoctormapping",
            constraint=models.UniqueConstraint(
                fields=("patient", "doctor"),
                name="unique_patient_doctor",
            ),
        ),
    ]
