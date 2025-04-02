from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
from typing import Dict, Tuple, List

class SentimentAnalysisService:
    """Service for sentiment analysis using a pre-trained BERT model"""
    
    def __init__(self):
        # Load pre-trained model and tokenizer
        self.model_name = "distilbert-base-uncased-finetuned-sst-2-english"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        
        # Define sentiment labels
        self.labels = ["negative", "positive"]
    
    def preprocess_text(self, text: str) -> str:
        """Preprocess text for sentiment analysis"""
        # Basic preprocessing
        text = text.lower().strip()
        return text
    
    def analyze_sentiment(self, text: str) -> Dict:
        """Analyze sentiment of a given text"""
        # Preprocess text
        text = self.preprocess_text(text)
        
        # Tokenize text
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Get model prediction
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probabilities = torch.nn.functional.softmax(logits, dim=1)
        
        # Convert to numpy for easier handling
        probs = probabilities.cpu().numpy()[0]
        
        # Get predicted label and confidence
        predicted_class = np.argmax(probs)
        confidence = probs[predicted_class]
        label = self.labels[predicted_class]
        
        # Convert to sentiment score between -1 and 1
        # For this model: 0 = negative, 1 = positive
        sentiment_score = (2 * probs[1] - 1)  # Maps [0,1] to [-1,1]
        
        # Determine sentiment label based on score
        if sentiment_score > 0.3:
            sentiment_label = "positive"
        elif sentiment_score < -0.3:
            sentiment_label = "negative"
        else:
            sentiment_label = "neutral"
        
        return {
            "sentiment_score": float(sentiment_score),
            "sentiment_label": sentiment_label,
            "confidence": float(confidence),
            "raw_probabilities": {
                "negative": float(probs[0]),
                "positive": float(probs[1])
            }
        }
    
    def analyze_batch(self, texts: List[str]) -> List[Dict]:
        """Analyze sentiment for a batch of texts"""
        results = []
        for text in texts:
            results.append(self.analyze_sentiment(text))
        return results

# Singleton instance
sentiment_service = SentimentAnalysisService()
