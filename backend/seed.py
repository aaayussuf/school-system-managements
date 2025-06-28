from app import create_app
from models.user import User
from models.student import Student
from models.fee import Fee
from models.attendance import Attendance
from models.timetable import Timetable
from datetime import datetime, date, time
import random

app = create_app()

def seed_database():
    with app.app_context():
        from app import db
        
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        # Create admin user
        admin = User(
            username='admin',
            email='admin@school.com',
            role='admin',
            is_active=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create teacher users
        teachers = []
        for i in range(1, 6):
            teacher = User(
                username=f'teacher{i}',
                email=f'teacher{i}@school.com',
                role='teacher',
                is_active=True
            )
            teacher.set_password(f'teacher{i}123')
            teachers.append(teacher)
            db.session.add(teacher)
        
        # Create student users and student records
        classes = ['Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 'Grade 5']
        for i in range(1, 21):
            student_user = User(
                username=f'student{i}',
                email=f'student{i}@school.com',
                role='student',
                is_active=True
            )
            student_user.set_password(f'student{i}123')
            db.session.add(student_user)
            db.session.flush()  # To get the user ID
            
            student = Student(
                user_id=student_user.id,
                full_name=f'Student {i}',
                student_id=f'STU{i:03d}',
                class_grade=random.choice(classes),
                guardian_name=f'Parent {i}',
                guardian_relation='Mother' if i % 2 == 0 else 'Father',
                address=f'{i} Main Street, City {i}',
                contact_number=f'555-{i:04d}'
            )
            db.session.add(student)
        
        db.session.commit()
        
        # Create fee records
        students = Student.query.all()
        terms = ['Term 1 2023', 'Term 2 2023', 'Term 1 2024']
        statuses = ['paid', 'unpaid', 'partial']
        
        for student in students:
            for term in terms:
                fee = Fee(
                    student_id=student.id,
                    amount=random.randint(100, 500),
                    payment_date=date(2023, random.randint(1, 12), random.randint(1, 28)) if random.choice([True, False]) else None,
                    due_date=date(2023, random.randint(1, 12), random.randint(1, 28)),
                    status=random.choice(statuses),
                    payment_method='Cash' if random.choice([True, False]) else 'Bank Transfer',
                    receipt_number=f'REC-{student.id}-{term[:5]}-{random.randint(1000, 9999)}',
                    academic_term=term,
                    description=f'Tuition fee for {term}'
                )
                db.session.add(fee)
        
        db.session.commit()
        
        # Create attendance records
        for student in students:
            for day in range(1, 30):
                attendance = Attendance(
                    student_id=student.id,
                    date=date(2023, random.randint(1, 12), day),
                    status=random.choice(['present', 'absent', 'late', 'excused']),
                    remarks='' if random.choice([True, False]) else 'Some remarks',
                    recorded_by=random.choice(teachers).id
                )
                db.session.add(attendance)
        
        db.session.commit()
        
        # Create timetable records
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        subjects = ['Math', 'Science', 'English', 'History', 'Geography', 'Art', 'Music', 'PE']
        
        for class_grade in classes:
            for day in days:
                for period in range(1, 6):
                    timetable = Timetable(
                        class_grade=class_grade,
                        day_of_week=day,
                        period_number=period,
                        subject=random.choice(subjects),
                        teacher_id=random.choice(teachers).id,
                        start_time=time(8 + period, 0),
                        end_time=time(8 + period, 50),
                        academic_term='Term 1 2024'
                    )
                    db.session.add(timetable)
        
        db.session.commit()
        
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_database()