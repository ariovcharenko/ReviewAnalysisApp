from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
import re
from typing import Dict, Tuple, List

class SentimentAnalysisService:
    """Service for sentiment analysis of smartphone reviews using a pre-trained BERT model"""
    
    def __init__(self):
        # Load pre-trained model and tokenizer
        self.model_name = "distilbert-base-uncased-finetuned-sst-2-english"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        
        # Define sentiment labels
        self.labels = ["negative", "positive"]
        
        # Define positive and negative keywords for rule-based adjustments
        self.positive_keywords = [
            "incredible", "amazing", "excellent", "great", "good", "love", "best", "perfect",
            "fantastic", "impressive", "outstanding", "superb", "brilliant", "awesome", 
            "wonderful", "exceptional", "superior", "terrific", "solid", "reliable", "quality",
            "premium", "fast", "quick", "responsive", "smooth", "clear", "crisp", "bright",
            "sharp", "beautiful", "impressed", "satisfied", "happy", "pleased", "recommend",
            "worth", "value", "efficient", "powerful", "convenient", "easy", "comfortable",
            "durable", "sturdy", "robust", "long-lasting"
        ]
        
        self.negative_keywords = [
            "bad", "poor", "terrible", "awful", "worst", "disappointing", "slow", "cheap",
            "horrible", "mediocre", "subpar", "inadequate", "inferior", "weak", "frustrating",
            "annoying", "useless", "waste", "regret", "avoid", "problem", "issue", "defect",
            "flaw", "broken", "fails", "failure", "struggles", "laggy", "lag", "sluggish",
            "unresponsive", "blurry", "grainy", "dim", "dull", "uncomfortable", "difficult",
            "hard", "heavy", "bulky", "fragile", "flimsy", "cheap", "overpriced", "expensive",
            "not worth", "disappointed", "unhappy", "dissatisfied", "complaint", "expected better",
            "not the best", "could be better", "not impressed", "drains", "hot", "overheats"
        ]
        
        # Define context phrases that imply sentiment
        self.context_phrases = {
            "positive": [
                "all day without", "lasts all day", "long battery", "bright and clear", 
                "under direct sunlight", "fast and responsive", "no lag", "haven't experienced any lag", 
                "apps open quickly", "feels premium", "impressed", "incredible", "fantastic", 
                "amazing", "love", "best", "excellent", "great", "perfect", "worth", "recommend", 
                "satisfied", "happy", "pleased"
            ],
            "negative": [
                "battery drain", "drains quickly", "drains fast", "charge twice", "have to charge",
                "scratches easily", "low light", "blurry", "not the best", "not up to par",
                "takes longer", "too long to", "not happy with", "gets hot", "overheats",
                "disappointed with", "struggles", "not worth", "expected better", "could be better",
                "not impressed", "disappointing", "poor", "terrible", "avoid", "regret", "issue", "problem"
            ]
        }
    
    def preprocess_text(self, text: str) -> str:
        """Preprocess text for sentiment analysis"""
        # Basic preprocessing
        text = text.lower().strip()
        return text
    
    def check_rule_based_sentiment(self, text: str) -> Dict:
        """Apply rule-based sentiment analysis for smartphone reviews"""
        text_lower = text.lower()
        
        # Check for context phrases first (they have higher priority)
        for phrase in self.context_phrases["positive"]:
            if phrase in text_lower:
                return {
                    "sentiment_score": 0.8,
                    "sentiment_label": "positive",
                    "rule_based": True
                }
        
        for phrase in self.context_phrases["negative"]:
            if phrase in text_lower:
                return {
                    "sentiment_score": -0.8,
                    "sentiment_label": "negative",
                    "rule_based": True
                }
        
        # Check for specific smartphone review patterns
        
        # Battery life positive patterns
        if re.search(r"battery.{1,30}(incredible|amazing|excellent|great|all day)", text_lower):
            return {
                "sentiment_score": 0.9,
                "sentiment_label": "positive",
                "rule_based": True
            }
        
        # Camera negative patterns
        if re.search(r"camera.{1,30}(struggles|low light|blurry|not the best)", text_lower):
            return {
                "sentiment_score": -0.7,
                "sentiment_label": "negative",
                "rule_based": True
            }
        
        # Overheating negative patterns
        if re.search(r"(gets? hot|overheats?|temperature).{1,30}(after|when|during)", text_lower):
            return {
                "sentiment_score": -0.8,
                "sentiment_label": "negative",
                "rule_based": True
            }
        
        # Performance positive patterns
        if re.search(r"(performance|speed).{1,30}(fast|responsive|no lag|smooth)", text_lower):
            return {
                "sentiment_score": 0.8,
                "sentiment_label": "positive",
                "rule_based": True
            }
        
        # Charging negative patterns
        if re.search(r"charging.{1,30}(takes longer|too long|expected|compared)", text_lower):
            return {
                "sentiment_score": -0.6,
                "sentiment_label": "negative",
                "rule_based": True
            }
        
        # Sound positive patterns
        if re.search(r"(sound|audio|speaker).{1,30}(fantastic|amazing|great|impressed)", text_lower):
            return {
                "sentiment_score": 0.9,
                "sentiment_label": "positive",
                "rule_based": True
            }
        
        # Camera negative patterns with disappointment
        if re.search(r"disappointed.{1,30}camera", text_lower) or re.search(r"camera.{1,30}disappointed", text_lower):
            return {
                "sentiment_score": -0.8,
                "sentiment_label": "negative",
                "rule_based": True
            }
        
        # Build quality positive patterns
        if re.search(r"(build|quality|feel).{1,30}(premium|excellent|great)", text_lower):
            return {
                "sentiment_score": 0.7,
                "sentiment_label": "positive",
                "rule_based": True
            }
        
        # Count positive and negative keywords
        positive_count = sum(1 for word in self.positive_keywords if word in text_lower)
        negative_count = sum(1 for word in self.negative_keywords if word in text_lower)
        
        # If there's a clear winner in the keyword count
        if positive_count > negative_count + 2:
            return {
                "sentiment_score": 0.6,
                "sentiment_label": "positive",
                "rule_based": True
            }
        elif negative_count > positive_count + 2:
            return {
                "sentiment_score": -0.6,
                "sentiment_label": "negative",
                "rule_based": True
            }
        
        # No rule-based decision
        return {
            "rule_based": False
        }
    
    def analyze_sentiment(self, text: str) -> Dict:
        """Analyze sentiment of a given text with enhanced smartphone review understanding"""
        # Preprocess text
        text = self.preprocess_text(text)
        
        # First check rule-based sentiment
        rule_based_result = self.check_rule_based_sentiment(text)
        
        # If we have a rule-based result, use it
        if rule_based_result.get("rule_based", False):
            # Add confidence and raw probabilities for API consistency
            rule_based_result["confidence"] = 0.9
            rule_based_result["raw_probabilities"] = {
                "negative": 0.5 - rule_based_result["sentiment_score"] / 2,
                "positive": 0.5 + rule_based_result["sentiment_score"] / 2
            }
            # Remove the rule_based flag
            del rule_based_result["rule_based"]
            return rule_based_result
        
        # Otherwise, use the model
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
        
        # Adjust sentiment score based on keywords
        text_lower = text.lower()
        
        # Count positive and negative keywords for fine-tuning
        positive_count = sum(1 for word in self.positive_keywords if word in text_lower)
        negative_count = sum(1 for word in self.negative_keywords if word in text_lower)
        
        # Adjust sentiment score based on keyword counts (smaller adjustment than rule-based)
        if positive_count > negative_count:
            sentiment_score = min(1.0, sentiment_score + 0.1 * (positive_count - negative_count))
        elif negative_count > positive_count:
            sentiment_score = max(-1.0, sentiment_score - 0.1 * (negative_count - positive_count))
        
        # Determine sentiment label based on adjusted score
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
