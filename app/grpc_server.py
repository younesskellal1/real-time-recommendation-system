import grpc
from concurrent import futures
import redis
import json
import logging
import os
import sys
import time

# Ajouter le répertoire parent au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.protos import recommendation_pb2
from app.protos import recommendation_pb2_grpc

class RecommendationServicer(recommendation_pb2_grpc.RecommendationServiceServicer):
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._initialize_test_data()

    def _initialize_test_data(self):
        """Initialiser des données de test dans Redis"""
        try:
            # Données de test pour les produits
            test_products = {
                'prod1': {'name': 'Smartphone X', 'category': 'electronics', 'price': '999'},
                'prod2': {'name': 'Laptop Pro', 'category': 'electronics', 'price': '1499'},
                'prod3': {'name': 'Python Programming', 'category': 'books', 'price': '49'},
                'prod4': {'name': 'Data Science Basics', 'category': 'books', 'price': '39'},
                'prod5': {'name': 'Wireless Earbuds', 'category': 'electronics', 'price': '199'}
            }

            # Ajouter les produits à Redis
            for prod_id, data in test_products.items():
                self.redis_client.hset(f"product:{prod_id}", mapping=data)

            # Ajouter des scores pour les produits tendance
            self.redis_client.zadd("trending:electronics", {
                'prod1': 100,
                'prod2': 80,
                'prod5': 60
            })

            self.redis_client.zadd("trending:books", {
                'prod3': 90,
                'prod4': 70
            })

            # Ajouter des produits populaires
            self.redis_client.zadd("popular_products", {
                'prod1': 100,
                'prod2': 90,
                'prod3': 80,
                'prod4': 70,
                'prod5': 60
            })

            self.logger.info("Test data initialized successfully")
        except Exception as e:
            self.logger.error(f"Error initializing test data: {e}")

    def GetRecommendations(self, request, context):
        try:
            user_id = request.user_id
            limit = request.limit
            categories = list(request.categories)

            recommendations = []
            
            if categories:
                for category in categories:
                    trending_key = f"trending:{category}"
                    trending_products = self.redis_client.zrevrange(trending_key, 0, limit-1, withscores=True)
                    
                    for product_id, score in trending_products:
                        product_data = self.redis_client.hgetall(f"product:{product_id}")
                        if product_data:
                            product = recommendation_pb2.Product(
                                id=product_id,
                                name=product_data.get('name', ''),
                                category=category,
                                score=float(score),
                                metadata=product_data
                            )
                            recommendations.append(product)
            else:
                popular_products = self.redis_client.zrevrange("popular_products", 0, limit-1, withscores=True)
                for product_id, score in popular_products:
                    product_data = self.redis_client.hgetall(f"product:{product_id}")
                    if product_data:
                        product = recommendation_pb2.Product(
                            id=product_id,
                            name=product_data.get('name', ''),
                            category=product_data.get('category', ''),
                            score=float(score),
                            metadata=product_data
                        )
                        recommendations.append(product)

            return recommendation_pb2.RecommendationResponse(
                products=recommendations,
                status="success",
                message="Recommendations retrieved successfully"
            )

        except Exception as e:
            self.logger.error(f"Error getting recommendations: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return recommendation_pb2.RecommendationResponse(
                status="error",
                message=str(e)
            )

    def UpdateUserPreferences(self, request, context):
        try:
            user_id = request.user_id
            favorite_categories = list(request.favorite_categories)
            category_weights = dict(request.category_weights)

            user_prefs = {
                'favorite_categories': json.dumps(favorite_categories),
                'category_weights': json.dumps(category_weights)
            }
            
            # Utiliser hset au lieu de hmset
            for key, value in user_prefs.items():
                self.redis_client.hset(f"user_prefs:{user_id}", key, value)
            
            self.redis_client.expire(f"user_prefs:{user_id}", 86400)  # 24 heures TTL

            return recommendation_pb2.UpdateResponse(
                success=True,
                message="User preferences updated successfully"
            )

        except Exception as e:
            self.logger.error(f"Error updating user preferences: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return recommendation_pb2.UpdateResponse(
                success=False,
                message=str(e)
            )

    def GetTrendingProducts(self, request, context):
        try:
            category = request.category
            limit = request.limit

            trending_key = f"trending:{category}"
            trending_products = self.redis_client.zrevrange(trending_key, 0, limit-1, withscores=True)

            products = []
            for product_id, score in trending_products:
                product_data = self.redis_client.hgetall(f"product:{product_id}")
                if product_data:
                    product = recommendation_pb2.Product(
                        id=product_id,
                        name=product_data.get('name', ''),
                        category=category,
                        score=float(score),
                        metadata=product_data
                    )
                    products.append(product)

            return recommendation_pb2.TrendingResponse(
                trending_products=products
            )

        except Exception as e:
            self.logger.error(f"Error getting trending products: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return recommendation_pb2.TrendingResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    recommendation_pb2_grpc.add_RecommendationServiceServicer_to_server(
        RecommendationServicer(), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve() 
    