from transformers import pipeline

# https://chatgpt.com/c/683ad42b-72c0-800d-b769-40ac072430b6

emotion_model = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)

def detect_emotion(text: str) -> str:
    scores = emotion_model(text)[0]
    top = max(scores, key=lambda x: x["score"])
    return top["label"]

# For multilingual detection (like Hindi, Tamil), we’ll later use xlm-roberta.