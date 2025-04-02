import spacy
from typing import List, Dict, Tuple
import re
from app.services.sentiment_service import sentiment_service

class AspectExtractionService:
    """Service for aspect-based sentiment analysis for smartphone reviews using SpaCy and BERT"""
    
    def __init__(self):
        # Load SpaCy model
        self.nlp = spacy.load("en_core_web_sm")
        
        # Smartphone-specific aspects with related terms
        self.smartphone_aspects = {
            "battery life": ["battery", "charge", "power", "last", "lasts", "lasting", "drain", "battery life"],
            "screen quality": ["screen", "display", "resolution", "brightness", "sunlight", "scratch", "screen quality"],
            "camera quality": ["camera", "photo", "picture", "image", "selfie", "lens", "zoom", "low light", "camera quality"],
            "performance": ["performance", "speed", "fast", "slow", "lag", "responsive", "snappy", "smooth", "processor", "cpu", "apps"],
            "sound quality": ["sound", "speaker", "audio", "volume", "loud", "music", "headphone", "bass", "sound quality"],
            "charging speed": ["charging", "charger", "fast charging", "quick charge", "power delivery", "usb-c", "charging speed"],
            "overheating": ["overheat", "hot", "heat", "temperature", "warm", "thermal", "cooling"],
            "build quality": ["build quality", "build", "premium", "design", "material", "feel", "weight", "heavy", "light", "plastic", "metal", "glass"]
        }
        
        # Flatten the aspects list for easier lookup
        self.all_aspects = []
        self.aspect_to_category = {}
        
        for category, terms in self.smartphone_aspects.items():
            for term in terms:
                self.all_aspects.append(term)
                self.aspect_to_category[term] = category
        
        # Context phrases that imply sentiment
        self.context_phrases = {
            "positive": [
                "all day", "lasts all day", "long battery", "bright and clear", "under direct sunlight",
                "fast and responsive", "no lag", "haven't experienced any lag", "apps open quickly",
                "feels premium", "impressed", "incredible", "fantastic", "amazing", "love", "best",
                "excellent", "great", "perfect", "worth", "recommend", "satisfied", "happy", "pleased"
            ],
            "negative": [
                "battery drain", "drains quickly", "drains fast", "charge twice", "have to charge",
                "scratches easily", "low light", "blurry", "not the best", "not up to par",
                "takes longer", "too long to", "not happy with", "gets hot", "overheats",
                "disappointed with", "struggles", "not worth", "expected better", "could be better",
                "not impressed", "disappointing", "poor", "terrible", "avoid", "regret", "issue", "problem"
            ]
        }
    
    def extract_aspects(self, text: str) -> List[Dict]:
        """Extract smartphone-specific aspects from text and analyze their sentiment"""
        # Process text with SpaCy
        doc = self.nlp(text)
        text_lower = text.lower()
        
        # Dictionary to store detected aspects and their sentiments
        detected_aspects = {}
        
        # First, check for direct aspect mentions
        for aspect_term in self.all_aspects:
            if aspect_term in text_lower:
                # Get the category for this aspect term
                category = self.aspect_to_category[aspect_term]
                
                # Find sentences containing the aspect
                sentences = [sent.text for sent in doc.sents if aspect_term in sent.text.lower()]
                
                if sentences:
                    # Use the first sentence containing the aspect
                    relevant_text = sentences[0]
                    
                    # Check for context phrases in the sentence
                    sentiment_override = None
                    
                    # Check positive context phrases
                    for phrase in self.context_phrases["positive"]:
                        if phrase in relevant_text.lower():
                            sentiment_override = "positive"
                            break
                    
                    # Check negative context phrases if no positive override
                    if not sentiment_override:
                        for phrase in self.context_phrases["negative"]:
                            if phrase in relevant_text.lower():
                                sentiment_override = "negative"
                                break
                    
                    # Analyze sentiment of the sentence
                    sentiment_result = sentiment_service.analyze_sentiment(relevant_text)
                    
                    # Apply sentiment override if found
                    if sentiment_override:
                        if sentiment_override == "positive":
                            sentiment_result["sentiment_score"] = max(0.5, sentiment_result["sentiment_score"])
                            sentiment_result["sentiment_label"] = "positive"
                        else:  # negative
                            sentiment_result["sentiment_score"] = min(-0.5, sentiment_result["sentiment_score"])
                            sentiment_result["sentiment_label"] = "negative"
                    
                    # Special case handling for specific phrases
                    if "incredible" in relevant_text.lower() and "battery" in relevant_text.lower():
                        sentiment_result["sentiment_score"] = 0.9
                        sentiment_result["sentiment_label"] = "positive"
                    
                    if "struggles" in relevant_text.lower() and "camera" in relevant_text.lower():
                        sentiment_result["sentiment_score"] = -0.7
                        sentiment_result["sentiment_label"] = "negative"
                    
                    if "overheats" in relevant_text.lower() or "gets hot" in relevant_text.lower():
                        sentiment_result["sentiment_score"] = -0.8
                        sentiment_result["sentiment_label"] = "negative"
                    
                    if "fast and responsive" in relevant_text.lower() and "performance" in relevant_text.lower():
                        sentiment_result["sentiment_score"] = 0.8
                        sentiment_result["sentiment_label"] = "positive"
                    
                    if "takes longer" in relevant_text.lower() and "charging" in relevant_text.lower():
                        sentiment_result["sentiment_score"] = -0.6
                        sentiment_result["sentiment_label"] = "negative"
                    
                    if "fantastic" in relevant_text.lower() and "sound" in relevant_text.lower():
                        sentiment_result["sentiment_score"] = 0.9
                        sentiment_result["sentiment_label"] = "positive"
                    
                    if "disappointed" in relevant_text.lower() and "camera" in relevant_text.lower():
                        sentiment_result["sentiment_score"] = -0.8
                        sentiment_result["sentiment_label"] = "negative"
                    
                    if "premium" in relevant_text.lower() and "build" in relevant_text.lower():
                        sentiment_result["sentiment_score"] = 0.7
                        sentiment_result["sentiment_label"] = "positive"
                    
                    # Store the result for this category
                    if category not in detected_aspects or abs(sentiment_result["sentiment_score"]) > abs(detected_aspects[category]["sentiment_score"]):
                        detected_aspects[category] = {
                            "aspect": category,
                            "sentiment_score": sentiment_result["sentiment_score"],
                            "sentiment_label": sentiment_result["sentiment_label"],
                            "confidence": sentiment_result["confidence"],
                            "relevant_text": relevant_text
                        }
        
        # Check for implied sentiments in the entire text
        # These are cases where the aspect might not be directly mentioned
        
        # Check for battery life implications
        if "all day without worrying" in text_lower and "battery life" not in detected_aspects:
            detected_aspects["battery life"] = {
                "aspect": "battery life",
                "sentiment_score": 0.8,
                "sentiment_label": "positive",
                "confidence": 0.9,
                "relevant_text": text
            }
        
        # Check for overheating implications
        if ("gets hot" in text_lower or "overheats" in text_lower) and "overheating" not in detected_aspects:
            detected_aspects["overheating"] = {
                "aspect": "overheating",
                "sentiment_score": -0.8,
                "sentiment_label": "negative",
                "confidence": 0.9,
                "relevant_text": text
            }
        
        # Convert the dictionary to a list of results
        results = list(detected_aspects.values())
        
        return results
    
    def analyze_aspects_batch(self, texts: List[str]) -> List[List[Dict]]:
        """Analyze aspects for a batch of texts"""
        results = []
        for text in texts:
            results.append(self.extract_aspects(text))
        return results

# Singleton instance
aspect_service = AspectExtractionService()
