"""
Google Gemini AI service for image recognition and product identification.
"""
import logging
import google.generativeai as genai
from django.conf import settings
from typing import Dict, Optional
from PIL import Image
import io

logger = logging.getLogger(__name__)


class GeminiService:
    """Service for interacting with Google Gemini API."""
    
    def __init__(self):
        """Initialize Gemini API."""
        if not settings.GEMINI_API_KEY:
            logger.warning("GEMINI_API_KEY not configured")
            self.model = None
            return
        
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def identify_product_from_image(self, image_data: bytes) -> Optional[Dict]:
        """
        Identify product from uploaded image using Gemini Vision API.
        
        Args:
            image_data: Image file bytes
            
        Returns:
            Dict with product name, brand, category, and features
        """
        if not self.model:
            logger.error("Gemini model not initialized")
            return None
        
        try:
            # Load image
            image = Image.open(io.BytesIO(image_data))
            
            # Create prompt for product identification
            prompt = """
            Analyze this product image and provide the following information in a structured format:
            
            1. Product Name: The specific name or type of the product
            2. Brand: The brand name if visible or identifiable
            3. Category: The product category (e.g., Electronics, Clothing, Home & Garden)
            4. Key Features: List 3-5 key features or characteristics
            5. Search Keywords: 5-7 keywords that would be useful for searching this product online
            
            Format your response as JSON with these keys:
            {
                "product_name": "...",
                "brand": "...",
                "category": "...",
                "features": ["...", "..."],
                "search_keywords": ["...", "..."],
                "confidence": "high/medium/low"
            }
            
            If you cannot identify the product clearly, return confidence as "low".
            """
            
            # Generate content with image
            response = self.model.generate_content([prompt, image])
            
            # Parse response
            result = self._parse_gemini_response(response.text)
            
            logger.info(f"Product identified: {result.get('product_name', 'Unknown')}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error identifying product from image: {str(e)}")
            return None
    
    def extract_product_info(self, text_description: str) -> Optional[Dict]:
        """
        Extract structured product information from text description.
        
        Args:
            text_description: Text description of the product
            
        Returns:
            Dict with extracted product information
        """
        if not self.model:
            logger.error("Gemini model not initialized")
            return None
        
        try:
            prompt = f"""
            Extract product information from this description and provide it in JSON format:
            
            Description: {text_description}
            
            Return JSON with these keys:
            {{
                "product_name": "...",
                "brand": "...",
                "category": "...",
                "features": ["...", "..."],
                "search_keywords": ["...", "..."]
            }}
            """
            
            response = self.model.generate_content(prompt)
            result = self._parse_gemini_response(response.text)
            
            return result
            
        except Exception as e:
            logger.error(f"Error extracting product info: {str(e)}")
            return None
    
    def generate_search_query(self, image_data: bytes) -> Optional[str]:
        """
        Generate optimized search query from product image.
        
        Args:
            image_data: Image file bytes
            
        Returns:
            Optimized search query string
        """
        product_info = self.identify_product_from_image(image_data)
        
        if not product_info:
            return None
        
        # Build search query from extracted information
        query_parts = []
        
        if product_info.get('brand'):
            query_parts.append(product_info['brand'])
        
        if product_info.get('product_name'):
            query_parts.append(product_info['product_name'])
        
        # Add key features
        features = product_info.get('features', [])
        if features:
            query_parts.extend(features[:2])  # Add top 2 features
        
        search_query = ' '.join(query_parts)
        logger.info(f"Generated search query: {search_query}")
        
        return search_query
    
    def compare_product_similarity(self, product_data: Dict, search_result: Dict) -> float:
        """
        Calculate similarity score between identified product and search result.
        
        Args:
            product_data: Product info from image recognition
            search_result: Product listing from scraper
            
        Returns:
            Similarity score (0-100)
        """
        if not self.model:
            return 0.0
        
        try:
            prompt = f"""
            Compare these two products and rate their similarity on a scale of 0-100:
            
            Product 1 (from image):
            - Name: {product_data.get('product_name', 'N/A')}
            - Brand: {product_data.get('brand', 'N/A')}
            - Features: {', '.join(product_data.get('features', []))}
            
            Product 2 (from search):
            - Title: {search_result.get('title', 'N/A')}
            
            Return only a number between 0-100 representing the similarity percentage.
            100 means identical products, 0 means completely different.
            """
            
            response = self.model.generate_content(prompt)
            
            # Extract numeric score
            import re
            match = re.search(r'\d+', response.text)
            if match:
                score = float(match.group())
                return min(max(score, 0), 100)  # Clamp between 0-100
            
            return 0.0
            
        except Exception as e:
            logger.error(f"Error comparing products: {str(e)}")
            return 0.0
    
    def _parse_gemini_response(self, response_text: str) -> Dict:
        """Parse Gemini API response text to extract JSON."""
        import json
        import re
        
        try:
            # Try to find JSON in the response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            
            if json_match:
                json_str = json_match.group()
                return json.loads(json_str)
            
            # If no JSON found, parse manually
            logger.warning("Could not find JSON in Gemini response, parsing manually")
            
            return {
                'product_name': self._extract_field(response_text, 'product_name') or 
                               self._extract_field(response_text, 'Product Name'),
                'brand': self._extract_field(response_text, 'brand') or 
                        self._extract_field(response_text, 'Brand'),
                'category': self._extract_field(response_text, 'category') or 
                           self._extract_field(response_text, 'Category'),
                'features': [],
                'search_keywords': [],
                'confidence': 'low'
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing Gemini JSON response: {str(e)}")
            return {
                'product_name': 'Unknown',
                'brand': '',
                'category': '',
                'features': [],
                'search_keywords': [],
                'confidence': 'low'
            }
    
    @staticmethod
    def _extract_field(text: str, field_name: str) -> Optional[str]:
        """Extract a field value from text."""
        import re
        
        pattern = rf'{field_name}[:\s]+([^\n]+)'
        match = re.search(pattern, text, re.IGNORECASE)
        
        if match:
            return match.group(1).strip()
        
        return None
