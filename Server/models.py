from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

metadata = MetaData()
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum('Admin', 'Teacher', 'Student', name='user_roles'), nullable=False)

    student = db.relationship('Student', backref='user', uselist=False)
    teacher = db.relationship('Teacher', backref='user', uselist=False)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'role': self.role,
        }

    def __repr__(self):
        return f"<User {self.id}: {self.email}>"

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)
    enrollment_date = db.Column(db.Date, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10))
    phone_number = db.Column(db.String(20))

    enrollments = db.relationship('Enrollment', backref='student', lazy=True)
    grades = db.relationship('Grade', backref='student', lazy=True)
    attendance_records = db.relationship('Attendance', backref='student', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'enrollment_date': self.enrollment_date,
            'date_of_birth': self.date_of_birth,
            'gender': self.gender,
            'phone_number': self.phone_number,
        }

    def __repr__(self):
        return f"<Student {self.id}: {self.name}>"

class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)

    courses = db.relationship('Course', backref='teacher', lazy=True)
    classes = db.relationship('Class', backref='teacher', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
        }

    def __repr__(self):
        return f"<Teacher {self.id}: {self.name}>"

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    schedule = db.Column(db.String(255))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)

    enrollments = db.relationship('Enrollment', backref='course', lazy=True)
    grades = db.relationship('Grade', backref='course', lazy=True)
    attendance_records = db.relationship('Attendance', backref='course', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'schedule': self.schedule,
            'teacher_id': self.teacher_id,
        }

    def __repr__(self):
        return f"<Course {self.id}: {self.name}>"

class Class(db.Model):
    __tablename__ = 'classes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    schedule = db.Column(db.String(255))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)

    students = db.relationship('Enrollment', backref='class', lazy=True)
    grades = db.relationship('Grade', backref='class', lazy=True)
    attendance_records = db.relationship('Attendance', backref='class', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'schedule': self.schedule,
            'teacher_id': self.teacher_id,
        }

    def __repr__(self):
        return f"<Class {self.id}: {self.name}>"

class Enrollment(db.Model):
    __tablename__ = 'enrollments'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'course_id': self.course_id,
            'class_id': self.class_id,
        }

    def __repr__(self):
        return f"<Enrollment {self.id}: Student {self.student_id} in Course {self.course_id} / Class {self.class_id}>"

class Grade(db.Model):
    __tablename__ = 'grades'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=True)
    grade = db.Column(db.String(10), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'course_id': self.course_id,
            'class_id': self.class_id,
            'grade': self.grade,
        }

    def __repr__(self):
        return f"<Grade {self.id}: Student {self.student_id} in Course {self.course_id} / Class {self.class_id} - Grade {self.grade}>"

class Attendance(db.Model):
    __tablename__ = 'attendance'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=True)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum('Present', 'Absent', 'Late', name='attendance_status'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'course_id': self.course_id,
            'class_id': self.class_id,
            'date': self.date,
            'status': self.status,
        }

    def __repr__(self):
        return f"<Attendance {self.id}: Student {self.student_id} in Course {self.course_id} / Class {self.class_id} on {self.date} - Status {self.status}>"
