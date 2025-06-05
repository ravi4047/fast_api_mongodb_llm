# Making an Emotion Handler for the Persona Cloning Project
# This will handle the emotions and sentiments of the user.
from transformers.pipelines import pipeline
from typing import List, Dict

from persona_cloning.models.emotion import EmotionScore

class EmotionHandler:
    def __init__(self):
        # Initialize the emotion classifier pipeline
        self.emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)
        # Initialize the sentiment classifier pipeline
        # self.sentiment_classifier = pipeline("text-classification", model="", return_all_scores=True)
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest",
            device=-1,
            return_all_scores=True
        )

    def detect_emotions(self, text: str)-> List[EmotionScore]: # -> List[Dict[str, float]]:
        """
        Detect emotions in the given text.
        
        Args:
            text (str): The input text to analyze.
        
        Returns:
            List[Dict[str, float]]: A list of dictionaries with emotion labels and their scores.
        """
        return self.emotion_classifier(text)
#     Output:
# [[{'label': 'anger', 'score': 0.004419783595949411},
#   {'label': 'disgust', 'score': 0.0016119900392368436},
#   {'label': 'fear', 'score': 0.0004138521908316761},
#   {'label': 'joy', 'score': 0.9771687984466553},
#   {'label': 'neutral', 'score': 0.005764586851000786},
#   {'label': 'sadness', 'score': 0.002092392183840275},
#   {'label': 'surprise', 'score': 0.008528684265911579}]]
    
    def detect_sentiments(self, text: str) -> List[Dict[str, float]]:
        """
        Detect sentiments in the given text.
        
        Args:
            text (str): The input text to analyze.
        
        Returns:
            List[Dict[str, float]]: A list of dictionaries with sentiment labels and their scores.
        """
        return self.sentiment_analyzer(text)
#     Output:
# [[{'label': 'negative', 'score': 0.00010000000500000001},
#   {'label': 'neutral', 'score': 0.00010000000500000001},
#   {'label': 'positive', 'score': 0.9998000264167786}]]
    
    # How to check that the emotion classifier is working?
    def check_emotion_classifier(self, text: str) -> str:
        """
        Check the emotion classifier with a sample text.
        
        Args:
            text (str): The input text to analyze.
        
        Returns:
            str: The detected emotion label with the highest score.
        """
        results = self.detect_emotions(text)
        if results:
            top_emotion = max(results[0], key=lambda x: x['score'])
            return f"Detected Emotion: {top_emotion['label']} with score {top_emotion['score']:.2f}"
        return "No emotions detected."
    
    # How to check that emotion classifier pipeline has been set up correctly?
    def check_sentiment_classifier(self, text: str) -> str:
        """
        Check the sentiment classifier with a sample text.
        
        Args:
            text (str): The input text to analyze.
        
        Returns:
            str: The detected sentiment label with the highest score.
        """
        results = self.detect_sentiments(text)
        if results:
            top_sentiment = max(results[0], key=lambda x: x['score'])
            return f"Detected Sentiment: {top_sentiment['label']} with score {top_sentiment['score']:.2f}"
        return "No sentiments detected."

# Should we use this EmotionHandler in the main application?
# Yes, we can use this EmotionHandler to analyze user inputs and respond accordingly.

# Ok do it
    
# Example usage:
# if __name__ == "__main__":
#     handler = EmotionHandler()