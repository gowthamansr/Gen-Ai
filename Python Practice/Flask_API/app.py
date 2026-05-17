from flask import Flask, request

app = Flask(__name__)

students = {}

# CREATE
@app.route("/students/<int:id>", methods=["POST"])
def add_student(id):

    data = request.json

    students[id] = data["name"]

    return students


# READ ALL
@app.route("/students", methods=["GET"])
def get_students():

    return students


# READ ONE
@app.route("/students/<int:id>", methods=["GET"])
def get_student(id):

    return {
        "id": id,
        "name": students.get(id)
    }


# UPDATE
@app.route("/students/<int:id>", methods=["PUT"])
def update_student(id):

    data = request.json

    students[id] = data["name"]

    return students


# DELETE
@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):

    if id in students:

        del students[id]

    return students


if __name__ == "__main__":
    app.run(debug=True)