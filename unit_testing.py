import requests
import pandas as pd
import textdistance

def send_message_to_rasa(user_message):
    url = "http://localhost:5005/webhooks/rest/webhook"
    payload = {
        "sender": "user",
        "message": user_message
    }
    response = requests.post(url, json=payload)
    messages = [message['text'] for message in response.json() if 'text' in message]
    bot_message = "\n".join(messages)
    return bot_message

def preprocess_string(s):
    return ' '.join(s.split())

def score_response(expected_answer, rasa_answer):
    expected_answer_sanitized = preprocess_string(expected_answer)
    rasa_answer_sanitized = preprocess_string(rasa_answer)
    
    # Calculate Monge-Elkan similarity
    similarity = textdistance.monge_elkan.normalized_similarity(expected_answer_sanitized.split(), rasa_answer_sanitized.split())

    return similarity

def test_rasa_with_csv(file_path):
    df = pd.read_csv(file_path)
    
    total_questions = len(df)
    total_score = 0

    
    for index, row in df.iterrows():
        question = row['Question']
        expected_answer = row['Answer']
        
        rasa_answer = send_message_to_rasa(question)
        score = score_response(expected_answer, rasa_answer)
        total_score += score
        
        print(f"Question: {question}")
        # print(f"Expected: {expected_answer}")
        # print(f"Rasa Answer: {rasa_answer}")
        print(f"Score: {score}")
        print("----------------------------")

    print(f"Total Questions: {total_questions}")
    print(f"Total Correct Answers: {total_score}")
    print(f"Accuracy: {total_score/total_questions * 100:.2f}%")

file_path = "sc_voter_faq.csv"
test_rasa_with_csv(file_path)
