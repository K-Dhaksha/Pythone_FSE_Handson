import os
import requests
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    enrollment_year = db.Column(db.Integer)
    department_id = db.Column(db.Integer)  # References department conceptually

    enrollments = db.relationship("Enrollment", backref="student", lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "enrollment_year": self.enrollment_year,
            "department_id": self.department_id
        }

class Enrollment(db.Model):
    __tablename__ = "enrollments"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    course_id = db.Column(db.Integer, nullable=False)  # Conceptual reference to Course Service
    grade = db.Column(db.String(2))

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "course_id": self.course_id,
            "grade": self.grade
        }

def create_app():
    app = Flask(__name__)
    # Resolve absolute path for database to ensure it's created inside the service folder
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, "students.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Course Service base URL for inter-service communication
    # In a real system, this might come from environment variables or service discovery
    COURSE_SERVICE_URL = os.environ.get("COURSE_SERVICE_URL", "http://localhost:5001")

    # Student CRUD routes
    @app.route("/api/students", methods=["GET"])
    @app.route("/api/students/", methods=["GET"])
    def get_students():
        students = Student.query.all()
        return jsonify([s.to_dict() for s in students])

    @app.route("/api/students", methods=["POST"])
    @app.route("/api/students/", methods=["POST"])
    def create_student():
        data = request.get_json() or {}
        required = ["first_name", "email"]
        for field in required:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400
        
        # Check email uniqueness
        existing = Student.query.filter_by(email=data["email"]).first()
        if existing:
            return jsonify({"error": f"Student with email {data['email']} already exists"}), 400

        student = Student(
            first_name=data["first_name"],
            last_name=data.get("last_name"),
            email=data["email"],
            enrollment_year=data.get("enrollment_year"),
            department_id=data.get("department_id")
        )
        db.session.add(student)
        db.session.commit()
        return jsonify(student.to_dict()), 201

    @app.route("/api/students/<int:id>", methods=["GET"])
    @app.route("/api/students/<int:id>/", methods=["GET"])
    def get_student(id):
        student = Student.query.get(id)
        if not student:
            return jsonify({"error": "Student not found"}), 404
        return jsonify(student.to_dict())

    @app.route("/api/students/<int:id>", methods=["PUT"])
    @app.route("/api/students/<int:id>/", methods=["PUT"])
    def update_student(id):
        student = Student.query.get(id)
        if not student:
            return jsonify({"error": "Student not found"}), 404

        data = request.get_json() or {}
        if "first_name" in data:
            student.first_name = data["first_name"]
        if "last_name" in data:
            student.last_name = data["last_name"]
        if "email" in data:
            if data["email"] != student.email:
                existing = Student.query.filter_by(email=data["email"]).first()
                if existing:
                    return jsonify({"error": f"Student with email {data['email']} already exists"}), 400
            student.email = data["email"]
        if "enrollment_year" in data:
            student.enrollment_year = data["enrollment_year"]
        if "department_id" in data:
            student.department_id = data["department_id"]

        db.session.commit()
        return jsonify(student.to_dict())

    @app.route("/api/students/<int:id>", methods=["DELETE"])
    @app.route("/api/students/<int:id>/", methods=["DELETE"])
    def delete_student(id):
        student = Student.query.get(id)
        if not student:
            return jsonify({"error": "Student not found"}), 404
        db.session.delete(student)
        db.session.commit()
        return jsonify({"message": "Student deleted successfully"}), 200

    # Enrollment route
    @app.route("/api/students/<int:id>/enroll", methods=["POST"])
    @app.route("/api/students/<int:id>/enroll/", methods=["POST"])
    def enroll_student(id):
        student = Student.query.get(id)
        if not student:
            return jsonify({"error": "Student not found"}), 404

        data = request.get_json() or {}
        if "course_id" not in data:
            return jsonify({"error": "course_id is required"}), 400
        
        course_id = data["course_id"]

        # Call Course Service to verify the course exists
        try:
            url = f"{COURSE_SERVICE_URL}/api/courses/{course_id}"
            response = requests.get(url, timeout=5)
            if response.status_code == 404:
                return jsonify({"error": f"Course with ID {course_id} does not exist"}), 400
            elif response.status_code != 200:
                return jsonify({
                    "error": f"Course Service returned unexpected status {response.status_code}"
                }), 500
        except requests.exceptions.ConnectionError:
            # Step 101: Handle the scenario where Course Service is unavailable
            return jsonify({
                "error": "Course Service is unavailable. Enrollment cannot be completed at this time."
            }), 503
        except requests.exceptions.RequestException as e:
            return jsonify({
                "error": f"An error occurred while communicating with Course Service: {str(e)}"
            }), 500

        # Check if enrollment already exists to prevent duplicate enrollment
        existing = Enrollment.query.filter_by(student_id=id, course_id=course_id).first()
        if existing:
            return jsonify({"error": "Student is already enrolled in this course", "enrollment": existing.to_dict()}), 400

        # Create enrollment
        enrollment = Enrollment(
            student_id=id,
            course_id=course_id,
            grade=data.get("grade")
        )
        db.session.add(enrollment)
        db.session.commit()

        return jsonify({
            "message": "Enrolled successfully",
            "enrollment": enrollment.to_dict()
        }), 201

    @app.route("/api/students/<int:id>/enrollments", methods=["GET"])
    @app.route("/api/students/<int:id>/enrollments/", methods=["GET"])
    def get_student_enrollments(id):
        student = Student.query.get(id)
        if not student:
            return jsonify({"error": "Student not found"}), 404
        
        enrollments = Enrollment.query.filter_by(student_id=id).all()
        return jsonify([e.to_dict() for e in enrollments])

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"status": "error", "message": "Resource not found"}), 404

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({"status": "error", "message": "Internal Server Error"}), 500

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5002, debug=True)
