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
        """Get all products"""
        try:
            products = [product.to_dict() for product in PRODUCTS_DB]
            return jsonify({
                'status': 'success',
                'products': products
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