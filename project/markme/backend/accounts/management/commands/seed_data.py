"""
Management command: python manage.py seed_data
Seeds the database with sample data matching the frontend mock data.
Creates: 1 org, 1 teacher, 2 students (with dummy face enrollments), and sample attendance logs.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random


class Command(BaseCommand):
    help = 'Seed database with sample data for development'

    def handle(self, *args, **options):
        from accounts.models import User, Organization, Teacher, Student
        from attendance.models import AttendanceLog, Notification

        self.stdout.write('🌱 Seeding sample data...')

        # Organization
        org, _ = Organization.objects.get_or_create(
            name='BSA Academy',
            defaults={
                'address': '123 School Street, Mumbai',
                'contact_email': 'info@bsaacademy.edu',
                'contact_phone': '+91 9876543210',
            }
        )
        self.stdout.write(f'  ✅ Organization: {org.name}')

        # Teacher
        teacher_user, created = User.objects.get_or_create(
            email='david.clark@example.com',
            defaults={
                'full_name': 'Mr. David Clark',
                'role': User.TEACHER,
                'phone': '+1 (555) 402-7788',
            }
        )
        if created:
            teacher_user.set_password('teacher123')
            teacher_user.save()

        teacher, _ = Teacher.objects.get_or_create(
            user=teacher_user,
            defaults={'subject': 'Mathematics', 'organization': org}
        )
        self.stdout.write(f'  ✅ Teacher: {teacher_user.full_name}')

        # Students
        students_data = [
            {
                'email': 'alex.rivera@example.com',
                'full_name': 'Alex Rivera',
                'phone': '+1 (555) 019-2041',
                'guardian_phone': '+1 (555) 019-2041',
                'guardian_email': 'alex.rivera@example.com',
                'roll_number': 'STU-001',
                'password': 'student123',
            },
            {
                'email': 'sarah.c@example.com',
                'full_name': 'Sarah Chen',
                'phone': '+1 (555) 302-1144',
                'guardian_phone': '+1 (555) 302-1144',
                'guardian_email': 'sarah.c@example.com',
                'roll_number': 'STU-002',
                'password': 'student123',
            },
        ]

        created_students = []
        for s_data in students_data:
            s_user, created = User.objects.get_or_create(
                email=s_data['email'],
                defaults={
                    'full_name': s_data['full_name'],
                    'role': User.STUDENT,
                    'phone': s_data['phone'],
                }
            )
            if created:
                s_user.set_password(s_data['password'])
                s_user.save()

            student, _ = Student.objects.get_or_create(
                user=s_user,
                defaults={
                    'roll_number': s_data['roll_number'],
                    'guardian_phone': s_data['guardian_phone'],
                    'guardian_email': s_data['guardian_email'],
                    'assigned_teacher': teacher,
                    'organization': org,
                    'face_registered': False,  # No real face data in seed
                }
            )
            created_students.append(student)
            self.stdout.write(f'  ✅ Student: {s_user.full_name}')

        # Attendance logs for the last 7 days
        from django.db import IntegrityError
        today = timezone.localdate()
        for student in created_students:
            for i in range(7, 0, -1):
                day = today - timedelta(days=i)
                if day.weekday() < 5:  # Weekdays only
                    log_status = 'PRESENT' if random.random() > 0.2 else 'ABSENT'
                    try:
                        log = AttendanceLog.objects.filter(student=student, date=day).first()
                        if log:
                            log.status = log_status
                            log.method = 'MANUAL'
                            log.save()
                        else:
                            AttendanceLog.objects.create(
                                student=student,
                                date=day,
                                status=log_status,
                                method='MANUAL',
                            )
                    except IntegrityError:
                        pass  # Already exists, skip
            self.stdout.write(f'  ✅ Attendance logs seeded for {student.user.full_name}')

        self.stdout.write(self.style.SUCCESS('\n✨ Sample data seeded successfully!'))
        self.stdout.write('\n📋 Login credentials:')
        self.stdout.write('  Admin:   admin@hajrihub.ai / admin1234')
        self.stdout.write('  Teacher: david.clark@example.com / teacher123')
        self.stdout.write('  Student: alex.rivera@example.com / student123')
        self.stdout.write('  Student: sarah.c@example.com / student123')
