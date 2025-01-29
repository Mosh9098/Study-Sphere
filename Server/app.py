from flask import Flask, request, jsonify, make_response
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS
from models import db, User, Student, Teacher, Course, Class, Grade, Enrollment, Attendance
from datetime import datetime

# Initialize the Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize CORS, Bcrypt, and Migrate
CORS(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)

# Index route
class Index(Resource):
    def get(self):
        return {"message": "Welcome to Study Sphere App"}

api.add_resource(Index, '/')

# CRUD operations for Users
class Users(Resource):
    def get(self):
        users = User.query.all()
        users_list = [user.to_dict() for user in users]
        return make_response(jsonify({"count": len(users_list), "users": users_list}), 200)

    def post(self):
        hashed_password = bcrypt.generate_password_hash(request.json.get("password")).decode('utf-8')
        new_user = User(
            email=request.json.get("email"),
            password=hashed_password,
            role=request.json.get("role")
        )
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify(new_user.to_dict()), 201)

class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return make_response(jsonify(user.to_dict()), 200)

    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        if request.json.get("email"):
            user.email = request.json.get("email")
        if request.json.get("password"):
            user.password = bcrypt.generate_password_hash(request.json.get("password")).decode('utf-8')
        if request.json.get("role"):
            user.role = request.json.get("role")
        db.session.commit()
        return make_response(jsonify(user.to_dict()), 200)

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return make_response("", 204)

api.add_resource(Users, '/users')
api.add_resource(UserResource, '/users/<int:user_id>')

# CRUD operations for Students
class Students(Resource):
    def get(self):
        students = Student.query.all()
        students_list = [student.to_dict() for student in students]
        return make_response(jsonify({"count": len(students_list), "students": students_list}), 200)

    def post(self):
        new_student = Student(
            user_id=request.json.get("user_id"),
            name=request.json.get("name"),
            enrollment_date=datetime.strptime(request.json.get("enrollment_date"), '%Y-%m-%d'),
            date_of_birth=datetime.strptime(request.json.get("date_of_birth"), '%Y-%m-%d'),
            gender=request.json.get("gender"),
            phone_number=request.json.get("phone_number")
        )
        db.session.add(new_student)
        db.session.commit()
        return make_response(jsonify(new_student.to_dict()), 201)

class StudentResource(Resource):
    def get(self, student_id):
        student = Student.query.get_or_404(student_id)
        return make_response(jsonify(student.to_dict()), 200)

    def put(self, student_id):
        student = Student.query.get_or_404(student_id)
        if request.json.get("name"):
            student.name = request.json.get("name")
        if request.json.get("enrollment_date"):
            student.enrollment_date = datetime.strptime(request.json.get("enrollment_date"), '%Y-%m-%d')
        if request.json.get("date_of_birth"):
            student.date_of_birth = datetime.strptime(request.json.get("date_of_birth"), '%Y-%m-%d')
        if request.json.get("gender"):
            student.gender = request.json.get("gender")
        if request.json.get("phone_number"):
            student.phone_number = request.json.get("phone_number")
        db.session.commit()
        return make_response(jsonify(student.to_dict()), 200)

    def delete(self, student_id):
        student = Student.query.get_or_404(student_id)
        db.session.delete(student)
        db.session.commit()
        return make_response("", 204)

api.add_resource(Students, '/students')
api.add_resource(StudentResource, '/students/<int:student_id>')

# CRUD operations for Teachers
class Teachers(Resource):
    def get(self):
        teachers = Teacher.query.all()
        teachers_list = [teacher.to_dict() for teacher in teachers]
        return make_response(jsonify({"count": len(teachers_list), "teachers": teachers_list}), 200)

    def post(self):
        new_teacher = Teacher(
            user_id=request.json.get("user_id"),
            name=request.json.get("name")
        )
        db.session.add(new_teacher)
        db.session.commit()
        return make_response(jsonify(new_teacher.to_dict()), 201)

class TeacherResource(Resource):
    def get(self, teacher_id):
        teacher = Teacher.query.get_or_404(teacher_id)
        return make_response(jsonify(teacher.to_dict()), 200)

    def put(self, teacher_id):
        teacher = Teacher.query.get_or_404(teacher_id)
        if request.json.get("name"):
            teacher.name = request.json.get("name")
        db.session.commit()
        return make_response(jsonify(teacher.to_dict()), 200)

    def delete(self, teacher_id):
        teacher = Teacher.query.get_or_404(teacher_id)
        db.session.delete(teacher)
        db.session.commit()
        return make_response("", 204)

api.add_resource(Teachers, '/teachers')
api.add_resource(TeacherResource, '/teachers/<int:teacher_id>')

# CRUD operations for Courses
class Courses(Resource):
    def get(self):
        courses = Course.query.all()
        courses_list = [course.to_dict() for course in courses]
        return make_response(jsonify({"count": len(courses_list), "courses": courses_list}), 200)

    def post(self):
        new_course = Course(
            name=request.json.get("name"),
            description=request.json.get("description"),
            schedule=request.json.get("schedule"),
            teacher_id=request.json.get("teacher_id")
        )
        db.session.add(new_course)
        db.session.commit()
        return make_response(jsonify(new_course.to_dict()), 201)

class CourseResource(Resource):
    def get(self, course_id):
        course = Course.query.get_or_404(course_id)
        return make_response(jsonify(course.to_dict()), 200)

    def put(self, course_id):
        course = Course.query.get_or_404(course_id)
        if request.json.get("name"):
            course.name = request.json.get("name")
        if request.json.get("description"):
            course.description = request.json.get("description")
        if request.json.get("schedule"):
            course.schedule = request.json.get("schedule")
        if request.json.get("teacher_id"):
            course.teacher_id = request.json.get("teacher_id")
        db.session.commit()
        return make_response(jsonify(course.to_dict()), 200)

    def delete(self, course_id):
        course = Course.query.get_or_404(course_id)
        db.session.delete(course)
        db.session.commit()
        return make_response("", 204)

api.add_resource(Courses, '/courses')
api.add_resource(CourseResource, '/courses/<int:course_id>')

# CRUD operations for Classes
class Classes(Resource):
    def get(self):
        classes = Class.query.all()
        classes_list = [cls.to_dict() for cls in classes]
        return make_response(jsonify({"count": len(classes_list), "classes": classes_list}), 200)

    def post(self):
        new_class = Class(
            name=request.json.get("name"),
            description=request.json.get("description"),
            schedule=request.json.get("schedule"),
            teacher_id=request.json.get("teacher_id")
        )
        db.session.add(new_class)
        db.session.commit()
        return make_response(jsonify(new_class.to_dict()), 201)

class ClassResource(Resource):
    def get(self, class_id):
        cls = Class.query.get_or_404(class_id)
        return make_response(jsonify(cls.to_dict()), 200)

    def put(self, class_id):
        cls = Class.query.get_or_404(class_id)
        if request.json.get("name"):
            cls.name = request.json.get("name")
        if request.json.get("description"):
            cls.description = request.json.get("description")
        if request.json.get("schedule"):
            cls.schedule = request.json.get("schedule")
        if request.json.get("teacher_id"):
            cls.teacher_id = request.json.get("teacher_id")
        db.session.commit()
        return make_response(jsonify(cls.to_dict()), 200)

    def delete(self, class_id):
        cls = Class.query.get_or_404(class_id)
        db.session.delete(cls)
        db.session.commit()
        return make_response("", 204)

api.add_resource(Classes, '/classes')
api.add_resource(ClassResource, '/classes/<int:class_id>')

# CRUD operations for Enrollments
class Enrollments(Resource):
    def get(self):
        enrollments = Enrollment.query.all()
        enrollments_list = [enrollment.to_dict() for enrollment in enrollments]
        return make_response(jsonify({"count": len(enrollments_list), "enrollments": enrollments_list}), 200)

    def post(self):
        new_enrollment = Enrollment(
            student_id=request.json.get("student_id"),
            course_id=request.json.get("course_id"),
            class_id=request.json.get("class_id")
        )
        db.session.add(new_enrollment)
        db.session.commit()
        return make_response(jsonify(new_enrollment.to_dict()), 201)

class EnrollmentResource(Resource):
    def get(self, enrollment_id):
        enrollment = Enrollment.query.get_or_404(enrollment_id)
        return make_response(jsonify(enrollment.to_dict()), 200)

    def put(self, enrollment_id):
        enrollment = Enrollment.query.get_or_404(enrollment_id)
        if request.json.get("student_id"):
            enrollment.student_id = request.json.get("student_id")
        if request.json.get("course_id"):
            enrollment.course_id = request.json.get("course_id")
        if request.json.get("class_id"):
            enrollment.class_id = request.json.get("class_id")
        db.session.commit()
        return make_response(jsonify(enrollment.to_dict()), 200)

    def delete(self, enrollment_id):
        enrollment = Enrollment.query.get_or_404(enrollment_id)
        db.session.delete(enrollment)
        db.session.commit()
        return make_response("", 204)

api.add_resource(Enrollments, '/enrollments')
api.add_resource(EnrollmentResource, '/enrollments/<int:enrollment_id>')

# CRUD operations for Grades
class Grades(Resource):
    def get(self):
        grades = Grade.query.all()
        grades_list = [grade.to_dict() for grade in grades]
        return make_response(jsonify({"count": len(grades_list), "grades": grades_list}), 200)

    def post(self):
        new_grade = Grade(
            student_id=request.json.get("student_id"),
            course_id=request.json.get("course_id"),
            class_id=request.json.get("class_id"),
            grade=request.json.get("grade")
        )
        db.session.add(new_grade)
        db.session.commit()
        return make_response(jsonify(new_grade.to_dict()), 201)

class GradeResource(Resource):
    def get(self, grade_id):
        grade = Grade.query.get_or_404(grade_id)
        return make_response(jsonify(grade.to_dict()), 200)

    def put(self, grade_id):
        grade = Grade.query.get_or_404(grade_id)
        if request.json.get("student_id"):
            grade.student_id = request.json.get("student_id")
        if request.json.get("course_id"):
            grade.course_id = request.json.get("course_id")
        if request.json.get("class_id"):
            grade.class_id = request.json.get("class_id")
        if request.json.get("grade"):
            grade.grade = request.json.get("grade")
        db.session.commit()
        return make_response(jsonify(grade.to_dict()), 200)

    def delete(self, grade_id):
        grade = Grade.query.get_or_404(grade_id)
        db.session.delete(grade)
        db.session.commit()
        return make_response("", 204)

api.add_resource(Grades, '/grades')
api.add_resource(GradeResource, '/grades/<int:grade_id>')

# CRUD operations for Attendance
class AttendanceRecords(Resource):
    def get(self):
        records = Attendance.query.all()
        records_list = [record.to_dict() for record in records]
        return make_response(jsonify({"count": len(records_list), "attendance_records": records_list}), 200)

    def post(self):
        new_record = Attendance(
            student_id=request.json.get("student_id"),
            course_id=request.json.get("course_id"),
            class_id=request.json.get("class_id"),
            date=datetime.strptime(request.json.get("date"), '%Y-%m-%d'),
            status=request.json.get("status")
        )
        db.session.add(new_record)
        db.session.commit()
        return make_response(jsonify(new_record.to_dict()), 201)

class AttendanceRecordResource(Resource):
    def get(self, record_id):
        record = Attendance.query.get_or_404(record_id)
        return make_response(jsonify(record.to_dict()), 200)

    def put(self, record_id):
        record = Attendance.query.get_or_404(record_id)
        if request.json.get("student_id"):
            record.student_id = request.json.get("student_id")
        if request.json.get("course_id"):
            record.course_id = request.json.get("course_id")
        if request.json.get("class_id"):
            record.class_id = request.json.get("class_id")
        if request.json.get("date"):
            record.date = datetime.strptime(request.json.get("date"), '%Y-%m-%d')
        if request.json.get("status"):
            record.status = request.json.get("status")
        db.session.commit()
        return make_response(jsonify(record.to_dict()), 200)

    def delete(self, record_id):
        record = Attendance.query.get_or_404(record_id)
        db.session.delete(record)
        db.session.commit()
        return make_response("", 204)

api.add_resource(AttendanceRecords, '/attendance')
api.add_resource(AttendanceRecordResource, '/attendance/<int:record_id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
