import streamlit as st
import requests

API_BASE_URL = 'http://127.0.0.1:8000/quizzes/'

# function to add the new question to the quiz

def add_question(quiz_id,question_text,answer):
    url = f"{API_BASE_URL}{quiz_id}/add_question/"
    
    data = {
        'text':question_text,
        'answer':answer
    }
    
    response = requests.post(url,json=data)
    
    if response.status_code == 201:
        # st.success('Question added successfully!')
        return True
    else:
        return False
def add_quiz(title):
    url = API_BASE_URL
    data = {
        'title':title
    }
    response = requests.post(url,json=data)
    if response.status_code == 201:
        return response.json()
    else:
        return None
    
def fetch_quizzes():
    response = requests.get(API_BASE_URL)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to Fetch Quizzes")
        return []
    
st.title("Welcome to Quiz Channel")

mode = st.sidebar.selectbox("Choose Mode", ["create Quiz", "Add Questions", "Play Quiz"])

# ------------------ CREATE QUIZ ------------------
if mode == "create Quiz":
    st.header("Create a New Quiz")

    new_quiz_title = st.text_input("Enter quiz title")
    if st.button("Create Quiz"):
        if new_quiz_title.strip():
            new_quiz = add_quiz(new_quiz_title)
            if new_quiz:
                st.success(f"Quiz '{new_quiz_title}' created successfully")
            else:
                st.error("Failed to create Quiz")
        else:
            st.error("Quiz Title cannot be empty")

# ------------------ ADD QUESTIONS ------------------
elif mode == "Add Questions":
    st.header("Add Question to Quiz")

    quizzes = fetch_quizzes()

    if quizzes:
        quiz_titles = [q["title"] for q in quizzes]
        selected_quiz_title = st.selectbox("Select a Quiz", quiz_titles)

        selected_quiz = next(q for q in quizzes if q["title"] == selected_quiz_title)

        question_text = st.text_input("Enter the Question Text:")

        answer = []
        for i in range(4):
            answer_text = st.text_input(f"Answer {i+1} Text", key=f"answer_text_{i}")
            is_correct = st.checkbox("Is this the correct answer?", key=f"is_correct_{i}")

            if answer_text.strip():
                answer.append({"text": answer_text.strip(), "is_correct": is_correct})

        if st.button("Add Question"):
            if question_text.strip() and len(answer) >= 1:
                ok = add_question(selected_quiz["id"], question_text.strip(), answer)
                if ok:
                    st.success("Question added successfully")
                else:
                    st.error("Failed to add Question")
            else:
                st.error("Please provide a question and at least one answer")
    else:
        st.warning("No quizzes available. Create a quiz first.")


                        
# Interface of play quizes
elif mode == "Play Quiz":
    st.header("Play Quiz")

    def fetch_question(quiz_id):
        response = requests.get(f"{API_BASE_URL}{quiz_id}/")
        if response.status_code == 200:
            # ✅ your serializer uses 'question' not 'questions'
            return response.json().get("question", [])
        else:
            st.error("Failed to fetch questions")
            return []

    quizzes = fetch_quizzes()
    if quizzes:
        quiz_titles = [q["title"] for q in quizzes]
        selected_quiz_title = st.selectbox("Select a Quiz", quiz_titles)

        if selected_quiz_title:
            selected_quiz = next(q for q in quizzes if q["title"] == selected_quiz_title)
            questions = fetch_question(selected_quiz["id"])

            if not questions:
                st.info("No questions found for this quiz.")
            else:
                for question in questions:
                    st.subheader(question["text"])

                    # ✅ answers are inside each question, key is 'answer'
                    answer_options = {a["id"]: a["text"] for a in question.get("answer", [])}

                    if not answer_options:
                        st.warning("No answers added for this question yet.")
                        continue

                    selected_answer_id = st.radio(
                        "Choose an answer:",
                        list(answer_options.keys()),
                        format_func=lambda x: answer_options[x],
                        key=f"q_{question['id']}"
                    )

                    if st.button("Submit Answer!", key=f"submit_{question['id']}"):
                        response = requests.post(
                            f"{API_BASE_URL}{selected_quiz['id']}/submit_answer/",
                            json={
                                "question_id": question["id"],
                                "answer_id": selected_answer_id
                            }
                        )

                        if response.status_code == 200:
                            st.success(response.json().get("result", "No results received."))
                        else:
                            st.error("Failed to submit answer")
    else:
        st.info("No quizzes available.")