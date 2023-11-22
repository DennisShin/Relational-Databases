# Initial imports
from flask import make_response, jsonify, request, g
from flask import Flask
from models import db, Student, Course, Enrollment

from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
migrate = Migrate(app, db)
db.init_app(app)

# Inital routes for API (GET, POST, PATCH, DELETE)

# GET route to access the API
@app.route("/")
def root():
    return "<h1>Flask application is active!</h1>"

# GET route to access the API entry point
@app.route("/api")
def api():
    return {"message" : "Welcome to my API!"}

########################################################
####################  STUDENT ROUTES  ##################
########################################################

# GET route to access all students
@app.get("/api/students")
def get_students():
    students = Student.query.all()
    data = [student.to_dict() for student in students]
    return make_response(jsonify(data), 200)


# GET route to access a single student by id
@app.get("/api/students/<int:id>")
def get_student_by_id(id: int):
    student = Student.query.filter(Student.id == id).first()
    if not student:
        return make_response(jsonify({"error": f"id {id} not found"}), 404)
    return make_response(jsonify(student.to_dict()), 200)


# POST route to create a new student
@app.post("/api/students")
def post_students():
    data = request.get_json()

    student = Student(
        fname=data["fname"], lname=data["lname"], grad_year=data["grad_year"]
    )

    db.session.add(student)
    db.session.commit()

    return make_response(jsonify(student.to_dict()), 201)


# PATCH route to update a single student by id
@app.patch("/api/students/<int:id>")
def patch_student(id: int):
    student = Student.query.filter(Student.id == id).first()
    if not student:
        return make_response(jsonify({"error": f"id {id} not found"}), 404)
    request_data = request.get_json()
    for key in request_data:
        setattr(student, key, request_data[key])
    db.session.add(student)
    db.session.commit()
    return make_response(jsonify(student.to_dict()), 200)


# DELETE route to delete a single student by id
@app.delete("/api/students/<int:id>")
def delete_student(id: int):
    student = Student.query.filter(Student.id == id).first()
    if not student:
        return make_response(jsonify({"error": f"id {id} not found"}), 404)
    db.session.delete(student)
    db.session.commit()

    return make_response(jsonify({}), 200)


########################################################
####################  COURSES ROUTES  ##################
########################################################

# GET route for accessing all courses
@app.get("/api/courses")
def get_courses():
    courses = Course.query.all()
    data = [course.to_dict() for course in courses]
    return make_response(jsonify(data), 200)


# GET route for accessing a single course by id
@app.get("/api/courses/<int:id>")
def get_course_by_id(id: int):
    course = Course.query.filter(Course.id == id).first()
    if not course:
        return make_response(jsonify({"error": f"id {id} not found"}), 404)
    return make_response(jsonify(course.to_dict()), 200)


# POST route for creating a new course
@app.post("/api/courses")
def post_courses():
    data = request.get_json()

    course = Course(
        title=data["title"], instructor=data["instructor"], credits=data["credits"]
    )

    db.session.add(course)
    db.session.commit()

    return make_response(jsonify(course.to_dict()), 201)


# PATCH route for updating a single course by id
@app.patch("/api/courses/<int:id>")
def patch_course(id: int):
    course = Course.query.filter(Course.id == id).first()
    if not course:
        return make_response(jsonify({"error": f"id {id} not found"}), 404)
    request_data = request.get_json()
    for key in request_data:
        setattr(course, key, request_data[key])
    db.session.add(course)
    db.session.commit()
    return make_response(jsonify(course.to_dict()), 200)


# DELETE route for deleting a single course by id
@app.delete("/api/courses/<int:id>")
def delete_course(id: int):
    course = Course.query.filter(Course.id == id).first()
    if not course:
        return make_response(jsonify({"error": f"id {id} not found"}), 404)
    db.session.delete(course)
    db.session.commit()

    return make_response(jsonify(course.to_dict()), 200)



##############################################################################
####################  ASSOCIATION METHODS FOR STUDENTS  ######################
##############################################################################

# Route to add a course to a student's currently enrolled courses ( list )
#   (Same concept as route to add a pizza to a customer's currently ordered pizzas)

# POST route to add a course to a student's currently enrolled courses
@app.post("/api/students/<int:id>/enrollments")
def enroll_student(id: int):
    try:
        # 1. Find the student that matches the given id from the URL/link.
        student = Student.query.filter(Student.id == id).first()
        # 2. Find the course that matches the given id from the request.
        # NOTE: My request will be neither a `Student()` or `Course()`. It will be an `Enrollment()`
        request_data = request.get_json()
        course = Course.query.filter(Course.id == request_data["course_id"]).first()
        # 3. Find our matching stident and course using a third object: Enrollment.
        enrollment = Enrollment(student_id=student.id, course_id = course.id)
        # 4. Add and commit changes to our database
        db.session.add(enrollment)
        db.session.commit()
        #  5. Return accepted value to our frontend/API
        return make_response(jsonify(enrollment), 200)
    except:
        return {"ERROR": "Something didn't want to work!"}


if __name__ == "__main__":
    app.run(port=5555, debug=True)