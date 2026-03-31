

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('specialty', models.CharField(choices=[('Cardiologist', 'Cardiologist'), ('Dermatologist', 'Dermatologist'), ('Neurologist', 'Neurologist'), ('Orthopedist', 'Orthopedist'), ('Pediatrician', 'Pediatrician'), ('Psychiatrist', 'Psychiatrist'), ('General Physician', 'General Physician'), ('ENT Specialist', 'ENT Specialist'), ('Ophthalmologist', 'Ophthalmologist'), ('Gynecologist', 'Gynecologist')], max_length=50)),
                ('hospital', models.CharField(max_length=150)),
                ('city', models.CharField(max_length=80)),
                ('experience_years', models.PositiveIntegerField(default=1)),
                ('phone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('fee', models.DecimalField(decimal_places=2, default=500.0, max_digits=8)),
                ('is_available', models.BooleanField(default=True)),
                ('latitude', models.FloatField(blank=True, help_text='For Google Maps', null=True)),
                ('longitude', models.FloatField(blank=True, help_text='For Google Maps', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Doctor',
                'verbose_name_plural': 'Doctors',
                'ordering': ['-created_at'],
            },
        ),
    ]