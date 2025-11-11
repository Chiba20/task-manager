from flask import Flask, jsonify, request

app = Flask(__name__)

# --------------------------
# Mock student database (mock data)
# Keys are strings to match query like ?id=12345
# --------------------------
students = {
    "12345": {"name": "Amina Omar", "course": "Computer Science", "year": 3, "gpa": 3.6},
    "23456": {"name": "Chiba Issa",   "course": "Information Systems", "year": 2, "gpa": 3.2},
    "34567": {"name": "Melanin Ahmed",   "course": "Mathematics", "year": 1, "gpa": 3.8},
    "45678": {"name": "Ali Hassan", "course": "Engineering", "year": 4, "gpa": 3.1}
}

# ------------------------------------------------------------
# /api/student?id=12345
# Returns: name, course, year, gpa
# ------------------------------------------------------------
@app.route("/api/student", methods=["GET"])
def get_student_by_id():
    student_id = request.args.get("id")
    if not student_id:
        return jsonify({"error": "id parameter is required"}), 400

    student = students.get(str(student_id))
    if not student:
        return jsonify({"error": "Student not found"}), 404

    # Return only the fields required by the assignment
    result = {
        "name": student["name"],
        "course": student["course"],
        "year": student["year"],
        "gpa": student["gpa"]
    }
    return jsonify(result)


# ------------------------------------------------------------
# /api/students/count
# Returns: total number of students (mock data)
# ------------------------------------------------------------
@app.route("/api/students/count", methods=["GET"])
def get_students_count():
    total = len(students)
    return jsonify({"total_students": total})


if __name__ == "__main__":
    # safe port (change if already used)
    app.run(debug=True, host="127.0.0.1", port=5002)
