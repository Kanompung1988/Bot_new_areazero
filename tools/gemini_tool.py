"""
Gemini API Tool for AI Research Bot
"""
import requests
import json
from typing import Dict, Any, Optional
import config
from utils.logger import get_logger

logger = get_logger(__name__)


class GeminiAPI:
    """Wrapper for Gemini API interactions"""
    
    def __init__(self):
        self.api_key = config.GEMINI_API_KEY
        self.api_url = config.GEMINI_API_URL
        self.headers = {
            'Content-Type': 'application/json',
            'X-goog-api-key': self.api_key
        }
    
    def generate_content(self, prompt: str, temperature: float = 0.7, max_tokens: Optional[int] = None) -> Optional[str]:
        """
        Generate content using Gemini API
        
        Args:
            prompt: The input prompt
            temperature: Controls randomness (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text or None if error
        """
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": temperature,
            }
        }
        
        if max_tokens:
            payload["generationConfig"]["maxOutputTokens"] = max_tokens
        
        try:
            logger.info(f"Calling Gemini API with prompt length: {len(prompt)}")
            response = requests.post(
                self.api_url,
                headers=self.headers,
                data=json.dumps(payload),
                timeout=60
            )
            response.raise_for_status()
            
            result = response.json()
            
            # Extract text from response
            if 'candidates' in result and len(result['candidates']) > 0:
                content = result['candidates'][0]['content']
                if 'parts' in content and len(content['parts']) > 0:
                    text = content['parts'][0]['text']
                    logger.info(f"Successfully generated {len(text)} characters")
                    return text
            
            logger.warning("No content generated from Gemini API")
            return None
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Gemini API request failed: {e}")
            return None
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            logger.error(f"Failed to parse Gemini API response: {e}")
            return None
    
    def summarize_text(self, text: str, max_sentences: int = 3) -> Optional[str]:
        """Summarize text to specified number of sentences"""
        prompt = f"""Summarize the following text in {max_sentences} sentences or less. 
Be concise and focus on the main points:

{text}

Summary:"""
        return self.generate_content(prompt, temperature=0.3)
    
    def rank_papers(self, papers: list) -> Optional[str]:
        """
        Analyze and rank papers by importance
        
        Args:
            papers: List of paper dicts with title, abstract, authors, etc.
            
        Returns:
            JSON string with ranked papers
        """
        papers_text = "\n\n".join([
            f"Paper {i+1}:\nTitle: {p.get('title', 'N/A')}\nAbstract: {p.get('abstract', 'N/A')[:500]}..."
            for i, p in enumerate(papers[:30])  # Limit to avoid token limits
        ])
        
        prompt = f"""You are an AI research expert. Analyze these recent AI papers and rank the top 10 most important, novel, and impactful ones.

Consider:
1. Novelty and innovation
2. Potential impact on the field
3. Practical applications
4. Research quality

Papers:
{papers_text}

Return ONLY a JSON array with the indices (1-based) of the top 10 papers in ranked order, along with a brief reason (max 20 words) for each.
Format: [{{"rank": 1, "paper_index": X, "reason": "..."}}, ...]

JSON:"""
        
        return self.generate_content(prompt, temperature=0.5, max_tokens=2000)
    
    def categorize_content(self, title: str, abstract: str) -> Optional[str]:
        """Categorize paper into AI topics"""
        prompt = f"""Categorize this AI paper into ONE primary category:
- LLM (Large Language Models)
- Computer Vision
- NLP (Natural Language Processing)
- Reinforcement Learning
- ML Theory
- AI Safety
- Robotics
- Other

Title: {title}
Abstract: {abstract[:300]}

Return ONLY the category name, nothing else."""
        
        return self.generate_content(prompt, temperature=0.1)
    
    def generate_intro_message(self, date: str) -> Optional[str]:
        """Generate engaging introduction for daily digest"""
        prompt = f"""Write a brief, engaging introduction (2-3 sentences) for a daily AI research digest for {date}.
Make it enthusiastic and highlight the excitement of staying updated with AI developments.
Keep it professional but friendly."""
        
        return self.generate_content(prompt, temperature=0.8)


# Singleton instance
_gemini_api = None

def get_gemini_api() -> GeminiAPI:
    """Get singleton instance of GeminiAPI"""
    global _gemini_api
    if _gemini_api is None:
        _gemini_api = GeminiAPI()
    return _gemini_api
