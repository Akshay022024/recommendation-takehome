import openai
from config import config

class LLMService:
    """
    Service to handle interactions with the LLM API
    """
    
    def __init__(self):
        """
        Initialize the LLM service with configuration
        """
        openai.api_key = config['OPENAI_API_KEY']
        self.model_name = config['MODEL_NAME']
        self.max_tokens = config['MAX_TOKENS']
        self.temperature = config['TEMPERATURE']
    
    def generate_recommendations(self, user_preferences, browsing_history, all_products):
        """
        Generate personalized product recommendations based on user preferences and browsing history
        
        Parameters:
        - user_preferences (dict): User's stated preferences
        - browsing_history (list): List of product IDs the user has viewed
        - all_products (list): Full product catalog
        
        Returns:
        - dict: Recommended products with explanations
        """
        # TODO: Implement LLM-based recommendation logic
        # This is where your prompt engineering expertise will be evaluated
        
        # Get browsed products details
        browsed_products = []
        for product_id in browsing_history:
            for product in all_products:
                if product["id"] == product_id:
                    browsed_products.append(product)
                    break
        
        # Create a prompt for the LLM
        # IMPLEMENT YOUR PROMPT ENGINEERING HERE
        prompt = self._create_recommendation_prompt(user_preferences, browsed_products, all_products)
        
        # Call the LLM API
        try:
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful eCommerce product recommendation assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            # Parse the LLM response to extract recommendations
            # IMPLEMENT YOUR RESPONSE PARSING LOGIC HERE
            recommendations = self._parse_recommendation_response(response.choices[0].message.content, all_products)
            
            return recommendations
            
        except Exception as e:
            # Handle any errors from the LLM API
            print(f"Error calling LLM API: {str(e)}")
            raise Exception(f"Failed to generate recommendations: {str(e)}")
    
    def _create_recommendation_prompt(self, user_preferences, browsed_products, all_products):
        """
        Create a prompt for the LLM to generate recommendations
        
        This is where you should implement your prompt engineering strategy.
        
        Parameters:
        - user_preferences (dict): User's stated preferences
        - browsed_products (list): Products the user has viewed
        - all_products (list): Full product catalog
        
        Returns:
        - str: Prompt for the LLM
        """
        # TODO: Implement your prompt engineering strategy
        # THIS FUNCTION MUST BE IMPLEMENTED BY THE CANDIDATE
        
        # Example basic prompt structure (you should significantly improve this):
        prompt = "Based on the following user preferences and browsing history, recommend 5 products from the catalog with explanations.\n\n"
        
        # Add user preferences to the prompt
        prompt += "User Preferences:\n"
        for key, value in user_preferences.items():
            prompt += f"- {key}: {value}\n"
        
        # Add browsing history to the prompt
        prompt += "\nBrowsing History:\n"
        for product in browsed_products:
            prompt += f"- {product['name']} (Category: {product['category']}, Price: ${product['price']})\n"
        
        # Add instructions for the response format
        prompt += "\nPlease recommend 5 products from the catalog that match the user's preferences and browsing history. For each recommendation, provide the product ID, name, and a brief explanation of why you're recommending it.\n"
        
        # Add response format instructions
        prompt += "\nFormat your response as a JSON array with objects containing 'product_id', 'explanation', and 'score' (1-10 indicating confidence)."
        
        # You would likely want to include the product catalog in the prompt
        # But be careful about token limits!
        # For a real implementation, you might need to filter the catalog to relevant products first
        
        return prompt
    
    def _parse_recommendation_response(self, llm_response, all_products):
        """
        Parse the LLM response to extract product recommendations
        
        Parameters:
        - llm_response (str): Raw response from the LLM
        - all_products (list): Full product catalog to match IDs with full product info
        
        Returns:
        - dict: Structured recommendations
        """
        # TODO: Implement response parsing logic
        # THIS FUNCTION MUST BE IMPLEMENTED BY THE CANDIDATE
        
        # Example implementation (very basic, should be improved):
        try:
            import json
            # Attempt to parse JSON from the response
            # Note: This is a simplistic approach and should be made more robust
            # The candidate should implement better parsing logic
            
            # Find JSON content in the response
            start_idx = llm_response.find('[')
            end_idx = llm_response.rfind(']') + 1
            
            if start_idx == -1 or end_idx == 0:
                # Fallback if JSON parsing fails
                return {
                    "recommendations": [],
                    "error": "Could not parse recommendations from LLM response"
                }
            
            json_str = llm_response[start_idx:end_idx]
            rec_data = json.loads(json_str)
            
            # Enrich recommendations with full product details
            recommendations = []
            for rec in rec_data:
                product_id = rec.get('product_id')
                product_details = None
                
                # Find the full product details
                for product in all_products:
                    if product['id'] == product_id:
                        product_details = product
                        break
                
                if product_details:
                    recommendations.append({
                        "product": product_details,
                        "explanation": rec.get('explanation', ''),
                        "confidence_score": rec.get('score', 5)
                    })
            
            return {
                "recommendations": recommendations,
                "count": len(recommendations)
            }
            
        except Exception as e:
            print(f"Error parsing LLM response: {str(e)}")
            return {
                "recommendations": [],
                "error": f"Failed to parse recommendations: {str(e)}"
            }