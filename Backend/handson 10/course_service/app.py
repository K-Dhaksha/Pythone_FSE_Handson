import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Department(db.Model):
    __tablename__ = "departments"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    head_of_dept = db.Column(db.String(100))
    budget = db.Column(db.Float)

    courses = db.relationship("Course", backref="department", lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "head_of_dept": self.head_of_dept,
            "budget": self.budget
        }

class Course(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "credits": self.credits,
            "department_id": self.department_id
        }

def create_app():
    app = Flask(__name__)
    # Resolve absolute path for database to ensure it's created inside the service folder
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, "courses.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Department routes
    @app.route("/api/departments", methods=["GET"])
    @app.route("/api/departments/", methods=["GET"])
    def get_departments():
        departments = Department.query.all()
        return jsonify([d.to_dict() for d in departments])

    @app.route("/api/departments", methods=["POST"])
    @app.route("/api/departments/", methods=["POST"])
    def create_department():
        data = request.get_json() or {}
        if "name" not in data:
            return jsonify({"error": "name is required"}), 400
        
        dept = Department(
            name=data["name"],
            head_of_dept=data.get("head_of_dept"),
            budget=data.get("budget")
        )
        db.session.add(dept)
        db.session.commit()
        return jsonify(dept.to_dict()), 201

    # Course routes
    @app.route("/api/courses", methods=["GET"])
    @app.route("/api/courses/", methods=["GET"])
    def get_courses():
        courses = Course.query.all()
        return jsonify([c.to_dict() for c in courses])

    @app.route("/api/courses", methods=["POST"])
    @app.route("/api/courses/", methods=["POST"])
    def create_course():
        data = request.get_json() or {}
        required = ["name", "code", "credits"]
        for field in required:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400
        
        # Check uniqueness of course code
        existing = Course.query.filter_by(code=data["code"]).first()
        if existing:
            return jsonify({"error": f"Course with code {data['code']} already exists"}), 400

        # Check if department_id is valid if provided
        dept_id = data.get("department_id")
        if dept_id:
            dept = Department.query.get(dept_id)
            if not dept:
                return jsonify({"error": f"Department with ID {dept_id} not found"}), 404

        course = Course(
            name=data["name"],
            code=data["code"],
            credits=data["credits"],
            department_id=dept_id
        )
        db.session.add(course)
        db.session.commit()
        return jsonify(course.to_dict()), 201

    @app.route("/api/courses/<int:id>", methods=["GET"])
    @app.route("/api/courses/<int:id>/", methods=["GET"])
    def get_course(id):
        course = Course.query.get(id)
        if not course:
            return jsonify({"error": "Course not found"}), 404
        return jsonify(course.to_dict())

    @app.route("/api/courses/<int:id>", methods=["PUT"])
    @app.route("/api/courses/<int:id>/", methods=["PUT"])
    def update_course(id):
        course = Course.query.get(id)
        if not course:
            return jsonify({"error": "Course not found"}), 404

        data = request.get_json() or {}
        if "name" in data:
            course.name = data["name"]
        if "code" in data:
            # Check uniqueness if code is updated
            if data["code"] != course.code:
                existing = Course.query.filter_by(code=data["code"]).first()
                if existing:
                    return jsonify({"error": f"Course with code {data['code']} already exists"}), 400
            course.code = data["code"]
        if "credits" in data:
            course.credits = data["credits"]
        if "department_id" in data:
            dept_id = data["department_id"]
            if dept_id:
                dept = Department.query.get(dept_id)
                if not dept:
                    return jsonify({"error": f"Department with ID {dept_id} not found"}), 404
            course.department_id = dept_id

        db.session.commit()
        return jsonify(course.to_dict())

    @app.route("/api/courses/<int:id>", methods=["DELETE"])
    @app.route("/api/courses/<int:id>/", methods=["DELETE"])
    def delete_course(id):
        course = Course.query.get(id)
        if not course:
            return jsonify({"error": "Course not found"}), 404
        db.session.delete(course)
        db.session.commit()
        return jsonify({"message": "Course deleted successfully"}), 200

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"status": "error", "message": "Resource not found"}), 404

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({"status": "error", "message": "Internal Server Error"}), 500

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5001, debug=True)
