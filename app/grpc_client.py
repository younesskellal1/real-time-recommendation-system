import grpc
import os
import sys

# Ajouter le répertoire parent au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.protos import recommendation_pb2
from app.protos import recommendation_pb2_grpc

def run():
    # Créer un canal gRPC
    with grpc.insecure_channel('localhost:50051') as channel:
        # Créer un stub (client)
        stub = recommendation_pb2_grpc.RecommendationServiceStub(channel)

        # Exemple d'appel pour obtenir des recommandations
        try:
            # Test GetRecommendations
            recommendation_request = recommendation_pb2.RecommendationRequest(
                user_id="user123",
                limit=5,
                categories=["electronics", "books"]
            )
            response = stub.GetRecommendations(recommendation_request)
            print("Recommendations received:")
            for product in response.products:
                print(f"- {product.name} (Score: {product.score})")

            # Test UpdateUserPreferences
            preferences = recommendation_pb2.UserPreferences(
                user_id="user123",
                favorite_categories=["electronics", "books"],
                category_weights={"electronics": 0.7, "books": 0.3}
            )
            update_response = stub.UpdateUserPreferences(preferences)
            print(f"\nUpdate preferences response: {update_response.message}")

            # Test GetTrendingProducts
            trending_request = recommendation_pb2.TrendingRequest(
                category="electronics",
                limit=3
            )
            trending_response = stub.GetTrendingProducts(trending_request)
            print("\nTrending products:")
            for product in trending_response.trending_products:
                print(f"- {product.name} (Score: {product.score})")

        except grpc.RpcError as e:
            print(f"RPC failed: {e}")

if __name__ == '__main__':
    run() 