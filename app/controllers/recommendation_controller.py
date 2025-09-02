from flask import jsonify, request
from app.services.recommendation_service import RecommendationService
from app.services.kafka_producer import KafkaEventProducer
from app.models.recommendation import ClickEvent
from app.models.product import PRODUCTS_DB
import time
import uuid

class RecommendationController:
    def __init__(self):
        self.recommendation_service = RecommendationService()
        self.kafka_producer = KafkaEventProducer()
    
    def get_products(self):
        """Get all products with pagination and optional search by name"""
        try:
            page = request.args.get('page', default=1, type=int)
            page_size = request.args.get('page_size', default=6, type=int)
            search = request.args.get('search', default='', type=str).strip().lower()

            # Filter products by name if search is provided
            if search:
                filtered_products = [product for product in PRODUCTS_DB if search in product.name.lower()]
            else:
                filtered_products = PRODUCTS_DB

            total = len(filtered_products)
            start = (page - 1) * page_size
            end = start + page_size
            products = [product.to_dict() for product in filtered_products[start:end]]
            return jsonify({
                'status': 'success',
                'products': products,
                'total': total,
                'page': page,
                'page_size': page_size
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    def track_click(self):
        """Track product click and send to Kafka"""
        try:
            data = request.get_json()
            product_id = data.get('product_id')
            category = data.get('category')
            
            if not product_id or not category:
                return jsonify({
                    'status': 'error',
                    'message': 'Missing product_id or category'
                }), 400
            
            # Create click event
            click_event = ClickEvent(
                product_id=product_id,
                category=category,
                timestamp=time.time(),
                session_id=str(uuid.uuid4())
            )
            
            # Send to Kafka
            success = self.kafka_producer.send_click_event(click_event)
            
            if success:
                return jsonify({
                    'status': 'success',
                    'message': 'Click tracked successfully'
                })
            else:
                return jsonify({
                    'status': 'error',
                    'message': 'Failed to track click'
                }), 500
                
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    def get_recommendations(self):
        """Get recommendations for a product"""
        try:
            product_id = request.args.get('product_id', type=int)
            limit = request.args.get('limit', default=5, type=int)
            
            if not product_id:
                return jsonify({
                    'status': 'error',
                    'message': 'Missing product_id parameter'
                }), 400
            
            recommendations = self.recommendation_service.get_recommendations(product_id, limit)
            
            return jsonify({
                'status': 'success',
                'recommendations': recommendations
            })
            
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500