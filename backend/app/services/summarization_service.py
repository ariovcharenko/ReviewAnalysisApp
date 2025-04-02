from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch
from typing import List, Dict

class SummarizationService:
    """Service for generating summaries of reviews using T5"""
    
    def __init__(self):
        # Load pre-trained model and tokenizer
        self.model_name = "t5-small"  # Can be upgraded to t5-base or t5-large for better quality
        self.tokenizer = T5Tokenizer.from_pretrained(self.model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(self.model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        
        # Maximum input length for T5
        self.max_input_length = 512
        
        # Maximum output length for summary
        self.max_output_length = 150
    
    def preprocess_text(self, text: str) -> str:
        """Preprocess text for summarization"""
        # T5 expects a "summarize: " prefix for summarization tasks
        text = "summarize: " + text.strip()
        return text
    
    def generate_summary(self, text: str) -> str:
        """Generate a summary for the given text"""
        # Preprocess text
        text = self.preprocess_text(text)
        
        # Tokenize text
        inputs = self.tokenizer(
            text, 
            return_tensors="pt", 
            max_length=self.max_input_length, 
            truncation=True
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Generate summary
        with torch.no_grad():
            output = self.model.generate(
                **inputs,
                max_length=self.max_output_length,
                num_beams=4,
                early_stopping=True
            )
        
        # Decode summary
        summary = self.tokenizer.decode(output[0], skip_special_tokens=True)
        
        return summary
    
    def generate_batch_summaries(self, texts: List[str]) -> List[str]:
        """Generate summaries for a batch of texts"""
        summaries = []
        for text in texts:
            summaries.append(self.generate_summary(text))
        return summaries

# Singleton instance
summarization_service = SummarizationService()
