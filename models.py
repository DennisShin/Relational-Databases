from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


"""
There are three major stops to giving life to our association table

1. Connact an individual physical object to the association table
    1a. `Student` <-> `Enrollment` ( This should also do `Enrollment` <-> `Student` in Flask)
    1b. `Course` <-> `Enrollment` ( This should also do `Enrollment` <-> `Course` in Flask)
2. Link the associations to the OTHER physical object
    2a. (`Student` <-> `Enrollment`) <---> `Course`
    2b. (`Course` <-> `Enrollment`) <---> `Student` 
3. Instruct our program(s) at every chance we get ( both in `models` and `app`)
    to not infinitely recurse/cascade when accessing nested data.
"""




# Setting up a database model for a student

class Student(db.Model, SerializerMixin):
    __tablename__ = "student_table"

    # When navigating across classes, stop after one level.
    # NOTE: "Once we've traversed the bridge (`enrollments`) back to the starting point (`student`), the gate closes."
    serialize_rules = ("-enrollments.student",)

    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String)
    lname = db.Column(db.String)
    grad_year = db.Column(db.Integer)

    # Relationship between a student and its enrollment association.
    # NOTE: This relationship needs to be closed back to the student-enrollment relationship.
    enrollments = db.relationship("Enrollment", back_populates="student")

    # This establishes a connection between TWO RELATIONSHIPS.
    # Specifically, I'm tethering the student-enrollment relationship to the course-enrollment relationship.
    courses = association_proxy("enrollments", "course")



# Setting up database model for a course.

class Course(db.Model, SerializerMixin):
    __tablename__ = "course_table"

    # When navigating across classes, stop after one level.
    # NOTE: "Once we've traversed the bridge (`enrollments`) back to the starting point (`course`), the gate closes."
    serialize_rules = ("-enrollments.course",)

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    instructor = db.Column(db.String)
    credits = db.Column(db.Integer)

    # Relationship between a course and its enrollment association.
    # NOTE: This relationship needs to be closed back to the course-enrollment relationship.
    enrollments = db.relationship("Enrollment", back_populates="course")

    # This establishes a connection between TWO RELATIONSHIPS.
    # Specifically, I'm tethering the course-enrollment relationship to the student-enrollment relationship.
    students = association_proxy("enrollments", "student")


# Setting up a database association model for connecting a student and a course
class Enrollment(db.Model, SerializerMixin):
    __tablename__ = "enrollment_table"

    # When navigating across classes, stop after one level.
    # NOTE: "A guard in the middle of the bridge that spots us initially crossing and knows to not let us cross again."
    serialize_rules = ("-student.enrollments","-course.enrollments")

    # Association table needs three IDs:
    #   -> `id`: The association table's primary key.
    #   -> `student_id`: A reference to the particular student.
    #   -> `course_id`: A reference to the particular course.
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student_table.id"))
    course_id = db.Column(db.Integer, db.ForeignKey("course_table.id"))

    # Set up the "invisible tether" (relationship) between a student and its enrollment.
    # NOTE: This should "backpopulate" or "close the loop" from the enrollment to the student.
    # NOTE: The attribute to backpopulate to (`enrollments`) MUST exist in the `Student` table.
    student = db.relationship("Student", back_populates="enrollments")
    # Set up the "invisible tether" (relationship) between a course and its enrollment.
    # NOTE: This should "backpopulate" or "close the loop" from the enrollment to the course.
    # NOTE: The attribute to backpopulate to (`enrollments`) MUST exist in the `Course` table.
    course = db.relationship("Course", back_populates="enrollments")
