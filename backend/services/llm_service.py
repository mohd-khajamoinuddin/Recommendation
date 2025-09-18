import google.generativeai as genai
from config import config

class LLMService:
    """
    Service to handle interactions with Gemini Flash 2.5 API
    """

    def __init__(self):
        """
        Initialize the LLM service with configuration
        """
        self.api_key = config['GEMINI_API_KEY']
        self.model_name = config.get('MODEL_NAME', 'gemini-1.5-flash-latest')
        self.max_tokens = config['MAX_TOKENS']
        self.temperature = config['TEMPERATURE']
        genai.configure(api_key=self.api_key)

    def generate_recommendations(self, user_preferences, browsing_history, all_products):
        """
        Generate personalized product recommendations based on user preferences and browsing history
        """
        # Get browsed products details
        browsed_products = [p for p in all_products if p["id"] in browsing_history]

        # Advanced prompt engineering
        prompt = self._create_recommendation_prompt(
            user_preferences, browsed_products, all_products
        )

        try:
            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": self.temperature,
                    "max_output_tokens": self.max_tokens,
                }
            )
            response_text = response.text if hasattr(response, 'text') else response.candidates[0].content.parts[0].text

            recommendations = self._parse_recommendation_response(response_text, all_products)
            return recommendations

        except Exception as e:
            print(f"Error calling Gemini API: {str(e)}")
            raise Exception(f"Failed to generate recommendations: {str(e)}")

    def _create_recommendation_prompt(self, user_preferences, browsed_products, all_products):
        """
        Create a prompt for Gemini to generate recommendations.
        """
        # To avoid context overflow, filter catalog to top 25 relevant products
        relevant_products = self._filter_catalog(user_preferences, all_products, limit=25)

        # Prompt structure
        prompt = (
            "You are an AI product recommender for an eCommerce site. "
            "Recommend 5 products from the provided catalog based on the user's preferences and browsing history. "
            "Give priority to products from the user's preferred categories. "
            "Each recommendation must include product_id, a short explanation, and a confidence score (1-10).\n\n"
            "User Preferences:\n"
        )
        for k, v in user_preferences.items():
            prompt += f"- {k}: {v}\n"

        prompt += "\nBrowsing History:\n"
        if browsed_products:
            for product in browsed_products:
                prompt += f"- {product['name']} (Category: {product['category']}, Price: ${product['price']})\n"
        else:
            prompt += "- (none)\n"

        prompt += (
            "\nProduct Catalog (each product as JSON):\n"
            + "\n".join([str({
                "id": p["id"], "name": p["name"], "category": p["category"],
                "subcategory": p.get("subcategory", ""), "price": p["price"],
                "brand": p["brand"], "tags": p.get("tags", []), "rating": p["rating"]
            }) for p in relevant_products])
        )

        prompt += (
            "\n\nPlease reply with a JSON array, each element having: "
            "{product_id, explanation, score}. Only recommend products from the provided catalog. "
            "Explain your reasoning for each recommendation."
        )

        return prompt

    def _filter_catalog(self, user_preferences, all_products, limit=25):
        """
        Filter the product catalog to the most relevant products for prompt context.
        """
        filtered = []
        for product in all_products:
            # Filter by category/brand/price if specified
            match_cat = not user_preferences.get('categories') or product['category'] in user_preferences['categories']
            match_brand = not user_preferences.get('brands') or product['brand'] in user_preferences['brands']
            match_price = True
            pr = user_preferences.get('priceRange', 'all')
            if pr != 'all':
                try:
                    if '-' in pr:
                        min_p, max_p = pr.split('-')
                        min_p = float(min_p) if min_p else 0
                        max_p = float(max_p) if max_p else float('inf')
                        match_price = min_p <= product['price'] <= max_p
                    else:
                        match_price = float(product['price']) >= float(pr)
                except Exception:
                    match_price = True
            if match_cat and match_brand and match_price:
                filtered.append(product)
        # Fallback: Return first N if no filters
        return filtered[:limit] if filtered else all_products[:limit]

    def _parse_recommendation_response(self, llm_response, all_products):
        """
        Parse Gemini's response to extract product recommendations.
        """
        import json
        try:
            start_idx = llm_response.find('[')
            end_idx = llm_response.rfind(']') + 1
            if start_idx == -1 or end_idx == 0:
                return {"recommendations": [], "error": "Could not parse recommendations from LLM response"}

            json_str = llm_response[start_idx:end_idx]
            rec_data = json.loads(json_str)

            recommendations = []
            for rec in rec_data:
                product_id = rec.get('product_id')
                product_details = next((p for p in all_products if p['id'] == product_id), None)
                if product_details:
                    recommendations.append({
                        "product": product_details,
                        "explanation": rec.get('explanation', ''),
                        "confidence_score": rec.get('score', 5)
                    })
            return {"recommendations": recommendations, "count": len(recommendations)}
        except Exception as e:
            print(f"Error parsing Gemini response: {str(e)}")
            return {
                "recommendations": [],
                "error": f"Failed to parse recommendations: {str(e)}"
            }