import spacy
from typing import List, Dict, Tuple
import re
from app.services.sentiment_service import sentiment_service

class AspectExtractionService:
    """Service for aspect-based sentiment analysis using SpaCy and BERT"""
    
    def __init__(self):
        # Load SpaCy model
        self.nlp = spacy.load("en_core_web_sm")
        
        # Common product aspects to look for
        self.common_aspects = {
            "electronics": [
                "battery", "screen", "display", "camera", "design", "build", "quality",
                "performance", "speed", "price", "value", "software", "app", "interface",
                "sound", "speaker", "connectivity", "wifi", "bluetooth", "durability",
                "reliability", "customer service", "support", "warranty", "charging",
                "storage", "memory", "processor", "cpu", "gpu", "graphics", "resolution",
                "weight", "size", "portability", "usability", "features", "functionality"
            ],
            "clothing": [
                "fabric", "material", "fit", "size", "comfort", "quality", "design", 
                "style", "color", "price", "value", "durability", "washing", "care"
            ],
            "food": [
                "taste", "flavor", "texture", "quality", "freshness", "price", "value",
                "portion", "size", "packaging", "delivery", "service", "ingredients"
            ]
        }
        
        # Flatten the aspects list
        self.all_aspects = []
        for category in self.common_aspects.values():
            self.all_aspects.extend(category)
        
        # Remove duplicates
        self.all_aspects = list(set(self.all_aspects))
    
    def extract_aspects(self, text: str) -> List[Dict]:
        """Extract aspects from text and analyze their sentiment"""
        # Process text with SpaCy
        doc = self.nlp(text)
        
        # Extract noun phrases as potential aspects
        noun_phrases = []
        for chunk in doc.noun_chunks:
            noun_phrases.append(chunk.text.lower())
        
        # Extract nouns as potential aspects
        nouns = [token.text.lower() for token in doc if token.pos_ == "NOUN"]
        
        # Combine and filter aspects
        extracted_aspects = set(noun_phrases + nouns)
        
        # Match with common aspects
        matched_aspects = {}
        for aspect in self.all_aspects:
            # Look for exact matches or matches within extracted aspects
            if aspect in extracted_aspects:
                matched_aspects[aspect] = aspect
            else:
                # Check if aspect is contained in any of the extracted aspects
                for extracted in extracted_aspects:
                    if aspect in extracted:
                        matched_aspects[aspect] = extracted
                        break
        
        results = []
        
        # For each matched aspect, find the relevant sentence and analyze sentiment
        for aspect, extracted in matched_aspects.items():
            # Find sentences containing the aspect
            sentences = [sent.text for sent in doc.sents if aspect in sent.text.lower() or extracted in sent.text.lower()]
            
            if sentences:
                # Use the first sentence containing the aspect
                relevant_text = sentences[0]
                
                # Analyze sentiment of the sentence
                sentiment_result = sentiment_service.analyze_sentiment(relevant_text)
                
                results.append({
                    "aspect": aspect,
                    "sentiment_score": sentiment_result["sentiment_score"],
                    "sentiment_label": sentiment_result["sentiment_label"],
                    "confidence": sentiment_result["confidence"],
                    "relevant_text": relevant_text
                })
        
        return results
    
    def analyze_aspects_batch(self, texts: List[str]) -> List[List[Dict]]:
        """Analyze aspects for a batch of texts"""
        results = []
        for text in texts:
            results.append(self.extract_aspects(text))
        return results

# Singleton instance
aspect_service = AspectExtractionService()
