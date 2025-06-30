import openai
from config import config

class LLMService:
    """
    Service to handle interactions with the LLM API
    
    This was challenging to get right - had to experiment with different prompt structures
    to get consistent JSON responses from the model. The key was being very explicit about
    the format and including examples in the prompt.
    """
    
    def __init__(self):
        """
        Initialize the LLM service with configuration
        """
        # Using OpenRouter for better model access and pricing
        # Spent some time debugging API endpoint issues before settling on this approach
        self.client = openai.OpenAI(
            api_key=config['OPENAI_API_KEY'],
            base_url=config.get('OPENAI_BASE_URL', 'https://api.openai.com/v1')
        )
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
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful and insightful AI shopping assistant for a modern e-commerce store. Your goal is to provide personalized product recommendations that genuinely match the user's needs."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                extra_headers={
                    "HTTP-Referer": "http://localhost:3000",
                    "X-Title": "i95dev Product Recommendations"
                }
            )
            
            # Parse the LLM response to extract recommendations
            # IMPLEMENT YOUR RESPONSE PARSING LOGIC HERE
            recommendations = self._parse_recommendation_response(response.choices[0].message.content, all_products)
            
            return recommendations
            
        except Exception as e:
            # Handle credit/payment errors specifically
            if "402" in str(e) or "credits" in str(e).lower():
                print(f"Credits insufficient, using fallback recommendations: {str(e)}")
                return self._generate_fallback_recommendations(user_preferences, browsed_products, all_products)
            else:
                # Handle any other errors from the LLM API
                print(f"Error calling LLM API: {str(e)}")
                return self._generate_fallback_recommendations(user_preferences, browsed_products, all_products)
    
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
        # Filter products based on preferences to reduce token usage
        relevant_products = self._filter_relevant_products(user_preferences, browsed_products, all_products)
        
        prompt = """You are an expert e-commerce product recommendation assistant. Your task is to analyze user preferences and browsing history to recommend the best 5 products from our catalog.

IMPORTANT: Respond with valid JSON only, no other text. Use this exact format:
[
  {
    "product_id": "prod001",
    "explanation": "This product matches your preferences because...",
    "score": 8.5
  }
]

**CRITICAL INSTRUCTIONS:**
1.  Respond ONLY with a valid JSON object in the specified format. Do not include any other text or explanations outside the JSON structure.
2.  Provide a unique, insightful reason for each recommendation.
3.  DO NOT recommend any products that are already in the user's browsing history.

USER PREFERENCES:"""
        
        # Add user preferences
        if user_preferences.get('priceRange') and user_preferences['priceRange'] != 'all':
            price_labels = {
                'under-50': 'Under $50',
                '50-100': '$50-$100',
                '100-200': '$100-$200',
                'over-200': 'Over $200'
            }
            prompt += f"\n- Budget: {price_labels.get(user_preferences['priceRange'], 'Any')}"
        
        if user_preferences.get('categories'):
            prompt += f"\n- Preferred Categories: {', '.join(user_preferences['categories'])}"
        
        if user_preferences.get('brands'):
            prompt += f"\n- Preferred Brands: {', '.join(user_preferences['brands'])}"
        
        # Add browsing history
        prompt += "\n\nBROWSING HISTORY (products they showed interest in):"
        if browsed_products:
            for product in browsed_products[-5:]:  # Last 5 browsed products
                prompt += f"\n- {product['name']} | {product['category']} | ${product['price']} | {product.get('brand', 'N/A')}"
        else:
            prompt += "\n- No browsing history yet"
        
        # Add product catalog (filtered)
        prompt += f"\n\nAVAILABLE PRODUCTS ({len(relevant_products)} products):"
        for product in relevant_products:
            features_str = ', '.join(product.get('features', [])[:3])
            prompt += f"\n- ID: {product['id']} | {product['name']} | {product['category']} | ${product['price']} | {product.get('brand', 'N/A')} | Features: {features_str}"
        
        prompt += """\n\nTASK:
1. Analyze the user's preferences and browsing patterns
2. Recommend exactly 5 products that best match their interests
3. For each recommendation, explain WHY it fits their preferences/behavior
4. Rate each recommendation 1-10 based on relevance
5. Consider variety - don't recommend only from one category unless they specifically prefer it

Return valid JSON array with product_id, explanation, and score fields."""
        
        return prompt
    
    def _filter_relevant_products(self, user_preferences, browsed_products, all_products):
        """Filter products to reduce token usage while keeping relevant ones"""
        relevant_products = []
        
        # Always include products from browsed categories/brands
        browsed_categories = set(p.get('category') for p in browsed_products)
        browsed_brands = set(p.get('brand') for p in browsed_products)
        
        for product in all_products:
            include = False
            
            # Include if matches user preferences
            if user_preferences.get('categories') and product['category'] in user_preferences['categories']:
                include = True
            if user_preferences.get('brands') and product.get('brand') in user_preferences['brands']:
                include = True
            
            # Include if from browsed categories/brands
            if product['category'] in browsed_categories or product.get('brand') in browsed_brands:
                include = True
            
            # Include if matches price range
            if user_preferences.get('priceRange') and user_preferences['priceRange'] != 'all':
                price = product['price']
                price_match = False
                if user_preferences['priceRange'] == 'under-50' and price < 50:
                    price_match = True
                elif user_preferences['priceRange'] == '50-100' and 50 <= price <= 100:
                    price_match = True
                elif user_preferences['priceRange'] == '100-200' and 100 <= price <= 200:
                    price_match = True
                elif user_preferences['priceRange'] == 'over-200' and price > 200:
                    price_match = True
                
                if price_match:
                    include = True
            
            # If no preferences set, include top-rated products
            if not user_preferences.get('categories') and not user_preferences.get('brands') and not browsed_products:
                if product.get('rating', 0) > 4.0:
                    include = True
            
            if include:
                relevant_products.append(product)
        
        # If we have too many, prioritize by rating and limit to 30 products
        if len(relevant_products) > 30:
            relevant_products.sort(key=lambda x: x.get('rating', 0), reverse=True)
            relevant_products = relevant_products[:30]
        
        # If we have too few, add some popular products
        if len(relevant_products) < 10:
            for product in all_products:
                if product not in relevant_products and product.get('rating', 0) > 4.0:
                    relevant_products.append(product)
                    if len(relevant_products) >= 20:
                        break
        
        return relevant_products
    
    def _parse_recommendation_response(self, llm_response, all_products):
        """
        Parse the LLM response to extract product recommendations
        
        Parameters:
        - llm_response (str): Raw response from the LLM
        - all_products (list): Full product catalog to match IDs with full product info
        
        Returns:
        - dict: Structured recommendations
        """
        try:
            import json
            import re
            
            # Clean the response - sometimes LLM adds extra text
            llm_response = llm_response.strip()
            
            # Find JSON content in the response
            json_match = re.search(r'\[.*\]', llm_response, re.DOTALL)
            if json_match:
                json_str = json_match.group()
            else:
                # Try to find JSON object array
                start_idx = llm_response.find('[')
                end_idx = llm_response.rfind(']') + 1
                
                if start_idx == -1 or end_idx == 0:
                    return {
                        "recommendations": [],
                        "count": 0,
                        "error": "No valid JSON found in LLM response"
                    }
                
                json_str = llm_response[start_idx:end_idx]
            
            # Parse JSON
            try:
                rec_data = json.loads(json_str)
            except json.JSONDecodeError as e:
                # Try to fix common JSON issues
                json_str = json_str.replace("'", '"')  # Single quotes to double quotes
                json_str = re.sub(r',\s*}', '}', json_str)  # Remove trailing commas
                json_str = re.sub(r',\s*]', ']', json_str)  # Remove trailing commas
                try:
                    rec_data = json.loads(json_str)
                except json.JSONDecodeError:
                    return {
                        "recommendations": [],
                        "count": 0,
                        "error": f"Failed to parse JSON: {str(e)}"
                    }
            
            if not isinstance(rec_data, list):
                return {
                    "recommendations": [],
                    "count": 0,
                    "error": "LLM response is not a JSON array"
                }
            
            # Process recommendations
            recommendations = []
            product_lookup = {p['id']: p for p in all_products}
            
            for rec in rec_data:
                if not isinstance(rec, dict):
                    continue
                product_id = rec.get('product_id')
                explanation = rec.get('explanation', 'No explanation provided')
                score = rec.get('score', 5.0)
                
                # Validate score
                try:
                    score = float(score)
                    if score < 1:
                        score = 1
                    elif score > 10:
                        score = 10
                except (ValueError, TypeError):
                    score = 5.0
                
                # Find the full product details
                product_details = product_lookup.get(product_id)
                
                if product_details:
                    recommendations.append({
                        "product": product_details,
                        "explanation": explanation,
                        "confidence_score": score
                    })
                else:
                    # Log missing product but don't fail
                    print(f"Warning: Product ID {product_id} not found in catalog")
            
            # Limit to 5 recommendations and sort by confidence
            recommendations.sort(key=lambda x: x['confidence_score'], reverse=True)
            recommendations = recommendations[:5]
            
            return {
                "recommendations": recommendations,
                "count": len(recommendations)
            }
            
        except Exception as e:
            print(f"Error parsing LLM response: {str(e)}")
            print(f"Raw response: {llm_response[:500]}...")  # Log first 500 chars for debugging
            
            # Fallback: return some random highly-rated products
            fallback_products = [p for p in all_products if p.get('rating', 0) > 4.5][:5]
            fallback_recommendations = []
            
            for i, product in enumerate(fallback_products):
                fallback_recommendations.append({
                    "product": product,
                    "explanation": f"Highly rated product in {product['category']} category (fallback recommendation)",
                    "confidence_score": 7.0 - (i * 0.5)  # Decreasing confidence
                })
            
            return {
                "recommendations": fallback_recommendations,
                "count": len(fallback_recommendations),
                "error": f"Used fallback recommendations due to parsing error: {str(e)}"
            }
    
    def _generate_fallback_recommendations(self, user_preferences, browsed_products, all_products):
        """
        Generate recommendations using rule-based logic when LLM API is unavailable
        """
        try:
            # Get relevant products based on preferences
            relevant_products = self._filter_relevant_products(user_preferences, browsed_products, all_products)
            
            # If no relevant products, use top-rated products
            if not relevant_products:
                relevant_products = sorted(all_products, key=lambda x: x.get('rating', 0), reverse=True)[:10]
            
            # Score products based on preferences and browsing history
            scored_products = []
            
            for product in relevant_products:
                score = 5.0  # Base score
                explanation_parts = []
                
                # Score based on user preferences
                if user_preferences.get('categories') and product['category'] in user_preferences['categories']:
                    score += 2.0
                    explanation_parts.append(f"matches your preferred {product['category']} category")
                
                if user_preferences.get('brands') and product.get('brand') in user_preferences['brands']:
                    score += 1.5
                    explanation_parts.append(f"from your preferred brand {product.get('brand')}")
                
                # Price preference matching
                if user_preferences.get('priceRange') and user_preferences['priceRange'] != 'all':
                    price = product['price']
                    price_match = False
                    if user_preferences['priceRange'] == 'under-50' and price < 50:
                        price_match = True
                    elif user_preferences['priceRange'] == '50-100' and 50 <= price <= 100:
                        price_match = True
                    elif user_preferences['priceRange'] == '100-200' and 100 <= price <= 200:
                        price_match = True
                    elif user_preferences['priceRange'] == 'over-200' and price > 200:
                        price_match = True
                    
                    if price_match:
                        score += 1.0
                        explanation_parts.append("fits your budget range")
                
                # Boost score for similar products to browsed ones
                browsed_categories = [p['category'] for p in browsed_products]
                if product['category'] in browsed_categories:
                    score += 1.5
                    explanation_parts.append("similar to products you've browsed")
                
                # Boost high-rated products
                rating = product.get('rating', 0)
                if rating > 4.5:
                    score += 1.0
                    explanation_parts.append(f"highly rated ({rating}/5)")
                elif rating > 4.0:
                    score += 0.5
                    explanation_parts.append(f"well-rated ({rating}/5)")
                
                # Create explanation
                if explanation_parts:
                    explanation = f"Recommended because it {', '.join(explanation_parts)}"
                else:
                    explanation = f"Popular {product['category']} product with good ratings"
                
                scored_products.append({
                    "product": product,
                    "score": min(score, 10.0),  # Cap at 10
                    "explanation": explanation
                })
            
            # Sort by score and take top 5
            scored_products.sort(key=lambda x: x['score'], reverse=True)
            top_recommendations = scored_products[:5]
            
            # Format for return
            recommendations = []
            for i, rec in enumerate(top_recommendations):
                recommendations.append({
                    "product": rec["product"],
                    "explanation": rec["explanation"],
                    "confidence_score": rec["score"]
                })
            
            return {
                "recommendations": recommendations,
                "count": len(recommendations),
                "fallback": True,
                "message": "Generated using intelligent fallback algorithm (LLM unavailable)"
            }
            
        except Exception as e:
            # Ultimate fallback - just return top-rated products
            top_products = sorted(all_products, key=lambda x: x.get('rating', 0), reverse=True)[:5]
            fallback_recommendations = []
            
            for i, product in enumerate(top_products):
                fallback_recommendations.append({
                    "product": product,
                    "explanation": f"Top-rated {product['category']} product (basic fallback)",
                    "confidence_score": 7.0 - (i * 0.5)
                })
            
            return {
                "recommendations": fallback_recommendations,
                "count": len(fallback_recommendations),
                "fallback": True,
                "error": f"Using basic fallback due to error: {str(e)}"
            }