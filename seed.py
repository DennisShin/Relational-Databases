from faker import Faker
from models import Student, Course, Enrollment
from random import choice, randint
from models import db
from app import app


fake = Faker()


def create_students():
    students = []
    for _ in range(10):
        fname = fake.name().split(" ")[0]
        lname = fake.name().split(" ")[1]
        students.append(
            Student(fname=fname, lname=lname, grad_year=randint(2023, 2027))
        )
    return students


def create_courses():
    courses = []
    for _ in range(10):
        word = fake.text().split(" ")[0]
        courses.append(
            Course(title=word, instructor=fake.name(), credits=choice([1, 3]))
        )
    return courses


def create_enrollments(students, courses):
    enrollments = []
    for _ in range(10):
        random_student = choice(students)
        random_course = choice(courses)
        enrollments.append(
            Enrollment(
                student_id = random_student.id,
                course_id = random_course.id
            )
        )
    return enrollments

with app.app_context():
    print("Seeding database...")
    Student.query.delete()
    Course.query.delete()
    Enrollment.query.delete()
    db.session.commit()

    print("Creating students...")
    students = create_students()
    db.session.add_all(students)
    db.session.commit()
    
    print("Creating courses...")
    courses = create_courses()
    db.session.add_all(courses)
    db.session.commit()

    print("Creating enrollments...")
    enrollments = create_enrollments(students, courses)
    db.session.add_all(enrollments)
    db.session.commit()


    print("Database Populated!")