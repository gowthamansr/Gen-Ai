import streamlit as st
import requests

st.title("Quiz App")

API_URL = "http://127.0.0.1:5000"

response = requests.get(f"{API_URL}/questions")

questions = response.json()

answers = []

for q in questions:

    st.subheader(q["question"])

    selected = st.radio(
        "Choose answer",
        q["options"],
        key=q["id"]
    )

    answers.append({
        "id": q["id"],
        "selected": selected
    })

if st.button("Submit Quiz"):

    result = requests.post(
        f"{API_URL}/submit",
        json={"answers": answers}
    )

    data = result.json()

    st.success(
        f"Score: {data['score']} / {data['total']}"
    )