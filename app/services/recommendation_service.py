import redis
import json
import time
from typing import List, Dict
from app.models.product import PRODUCTS_DB, Product
from app.models.recommendation import Recommendation
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class RecommendationService:
    def __init__(self, redis_host='localhost', redis_port=6379):
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
        self.products = {p.id: p for p in PRODUCTS_DB}
        self._build_similarity_matrix()
    
    def _build_similarity_matrix(self):
        """Build product similarity matrix using TF-IDF"""
        product_features = []
        product_ids = []
        
        for product in PRODUCTS_DB:
            # Combine category, tags, and description for similarity
            features = f"{product.category} {' '.join(product.tags)} {product.description}"
            product_features.append(features)
            product_ids.append(product.id)
        
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(product_features)
        self.similarity_matrix = cosine_similarity(tfidf_matrix)
        self.product_id_to_index = {pid: idx for idx, pid in enumerate(product_ids)}
    
    def get_recommendations(self, product_id: int, limit: int = 5) -> List[Dict]:
        """Get recommendations based on product similarity and category trends"""
        if product_id not in self.products:
            return []
        
        clicked_product = self.products[product_id]
        
        # Get content-based recommendations
        content_recs = self._get_content_based_recommendations(product_id, limit)
        
        # Get category-based recommendations (trending in same category)
        category_recs = self._get_category_trending_recommendations(clicked_product.category, limit)
        
        # Combine and deduplicate recommendations
        all_recs = {}
        
        # Add content-based recommendations with higher weight
        for rec in content_recs:
            if rec.product_id != product_id:
                all_recs[rec.product_id] = rec
        
        # Add category trending recommendations
        for rec in category_recs:
            if rec.product_id != product_id and rec.product_id not in all_recs:
                all_recs[rec.product_id] = rec
        
        # Sort by score and return top recommendations
        sorted_recs = sorted(all_recs.values(), key=lambda x: x.score, reverse=True)
        
        # Convert to dict format with product details
        recommendations = []
        for rec in sorted_recs[:limit]:
            product = self.products[rec.product_id]
            recommendations.append({
                'product': product.to_dict(),
                'score': rec.score,
                'reason': rec.reason
            })
        
        return recommendations
    
    def _get_content_based_recommendations(self, product_id: int, limit: int) -> List[Recommendation]:
        """Get recommendations based on product similarity"""
        if product_id not in self.product_id_to_index:
            return []
        
        product_idx = self.product_id_to_index[product_id]
        similarity_scores = self.similarity_matrix[product_idx]
        
        # Get top similar products
        similar_indices = np.argsort(similarity_scores)[::-1][1:limit+5]  # Exclude self
        
        recommendations = []
        for idx in similar_indices:
            if len(recommendations) >= limit:
                break
            
            similar_product_id = list(self.product_id_to_index.keys())[idx]
            score = similarity_scores[idx]
            
            if score > 0.1:  # Minimum similarity threshold
                recommendations.append(Recommendation(
                    product_id=similar_product_id,
                    score=score * 0.8,  # Content-based score weight
                    reason="Similar to your viewed product"
                ))
        
        return recommendations
    
    def _get_category_trending_recommendations(self, category: str, limit: int) -> List[Recommendation]:
        """Get trending products in the same category"""
        # Get recent clicks for this category from Redis
        category_clicks = self._get_category_clicks(category)
        
        # Score products based on recent popularity and rating
        category_products = [p for p in PRODUCTS_DB if p.category == category]
        scored_products = []
        
        for product in category_products:
            clicks_score = category_clicks.get(str(product.id), 0) * 0.3
            rating_score = product.rating * 0.2
            total_score = clicks_score + rating_score
            
            if total_score > 0:
                scored_products.append(Recommendation(
                    product_id=product.id,
                    score=total_score,
                    reason=f"Trending in {category}"
                ))
        
        # Sort by score and return top recommendations
        scored_products.sort(key=lambda x: x.score, reverse=True)
        return scored_products[:limit]
    
    def _get_category_clicks(self, category: str) -> Dict[str, int]:
        """Get recent click counts for products in a category"""
        try:
            clicks_data = self.redis_client.hgetall(f"category_clicks:{category}")
            return {k: int(v) for k, v in clicks_data.items()}
        except:
            return {}
    
    def update_click_stats(self, click_event: Dict):
        """Update click statistics in Redis"""
        try:
            product_id = str(click_event['product_id'])
            category = click_event['category']
            
            # Increment category click count
            self.redis_client.hincrby(f"category_clicks:{category}", product_id, 1)
            
            # Set expiration for click data (1 hour)
            self.redis_client.expire(f"category_clicks:{category}", 3600)
            
            # Store recent click for real-time processing
            click_key = f"recent_clicks:{int(time.time())}"
            self.redis_client.setex(click_key, 300, json.dumps(click_event))  # 5 min expiry
            
        except Exception as e:
            print(f"Error updating click stats: {e}")