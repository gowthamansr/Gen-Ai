from flask import Flask, jsonify, request

app = Flask(__name__)

questions = [
     {
        "id": 1,
        "question": "Python is a ?",
        "options": [
            "Programming Language",
            "Database",
            "Browser",
            "Game"
        ],
        "answer": "Programming Language"
    },
    {
        "id": 2,
        "question": "Which keyword is used for function?",
        "options": [
            "func",
            "define",
            "def",
            "function"
        ],
        "answer": "def"
    },
    {
        "id": 3,
        "question": "Which data type stores multiple values?",
        "options": [
            "int",
            "list",
            "float",
            "bool"
        ],
        "answer": "list"
    },
    {
        "id": 4,
        "question": "Which loop repeats while condition is True?",
        "options": [
            "for",
            "while",
            "loop",
            "repeat"
        ],
        "answer": "while"
    },
    {
        "id": 5,
        "question": "Which symbol is used for comments?",
        "options": [
            "//",
            "#",
            "/*",
            "--"
        ],
        "answer": "#"
    },
    {
        "id": 6,
        "question": "Capital of India?",
        "options": [
            "Delhi",
            "Mumbai",
            "Chennai",
            "Kolkata"
        ],
        "answer": "Delhi"
    },
    {
        "id": 7,
        "question": "Largest planet?",
        "options": [
            "Earth",
            "Mars",
            "Jupiter",
            "Venus"
        ],
        "answer": "Jupiter"
    },
    {
        "id": 8,
        "question": "Who invented telephone?",
        "options": [
            "Newton",
            "Einstein",
            "Alexander Graham Bell",
            "Tesla"
        ],
        "answer": "Alexander Graham Bell"
    },
    {
        "id": 9,
        "question": "National animal of India?",
        "options": [
            "Lion",
            "Elephant",
            "Tiger",
            "Leopard"
        ],
        "answer": "Tiger"
    },
    {
        "id": 10,
        "question": "How many continents?",
        "options": [
            "5",
            "6",
            "7",
            "8"
        ],
        "answer": "7"
    },
    {
        "id": 11,
        "question": "2 + 2 = ?",
        "options": [
            "3",
            "4",
            "5",
            "6"
        ],
        "answer": "4"
    },
    {
        "id": 12,
        "question": "10 × 5 = ?",
        "options": [
            "15",
            "50",
            "40",
            "60"
        ],
        "answer": "50"
    },
    {
        "id": 13,
        "question": "Square root of 81?",
        "options": [
            "8",
            "9",
            "7",
            "6"
        ],
        "answer": "9"
    },
    {
        "id": 14,
        "question": "100 / 5 = ?",
        "options": [
            "10",
            "20",
            "25",
            "15"
        ],
        "answer": "20"
    },
    {
        "id": 15,
        "question": "5² = ?",
        "options": [
            "10",
            "20",
            "25",
            "15"
        ],
        "answer": "25"
    }
]

# GET all questions
@app.route("/questions", methods=["GET"])
def get_questions():

    quiz_questions = []

    for q in questions:

        quiz_questions.append({
            "id": q["id"],
            "question": q["question"],
            "options": q["options"]
        })

    return jsonify(quiz_questions)


# POST submit answers
@app.route("/submit", methods=["POST"])
def submit_quiz():

    data = request.json

    score = 0

    for answer in data["answers"]:

        question_id = answer["id"]

        selected = answer["selected"]

        for q in questions:

            if q["id"] == question_id:

                if q["answer"] == selected:
                    score += 1

    return jsonify({
        "score": score,
        "total": len(questions)
    })


if __name__ == "__main__":
    app.run(debug=True)