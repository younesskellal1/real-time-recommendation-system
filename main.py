# main.py
from flask import Flask
from flask_cors import CORS
from app.views.api import api_bp
from app.services.kafka_consumer import KafkaEventConsumer
from app.services.recommendation_service import RecommendationService
import logging
import os
import threading
import time

def create_app():
    """Create and configure Flask app"""
    app = Flask(__name__, template_folder='app/templates')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    # Enable CORS
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(api_bp)
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    return app

def start_kafka_consumer():
    """Start Kafka consumer in background thread"""
    def consume_clicks(click_event):
        """Callback function to process consumed click events"""
        try:
            recommendation_service = RecommendationService()
            recommendation_service.update_click_stats(click_event)
            logging.info(f"Processed click event: {click_event}")
        except Exception as e:
            logging.error(f"Error processing click event: {e}")
    
    # Wait for Kafka to be ready
    time.sleep(10)
    
    try:
        consumer = KafkaEventConsumer()
        consumer.start_consuming(consume_clicks)
        logging.info("Kafka consumer started successfully")
    except Exception as e:
        logging.error(f"Failed to start Kafka consumer: {e}")

if __name__ == '__main__':
    # Create Flask app
    app = create_app()
    
    # Start Kafka consumer in background
    consumer_thread = threading.Thread(target=start_kafka_consumer, daemon=True)
    consumer_thread.start()
    
    # Start Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=os.environ.get('FLASK_ENV') == 'development'
    )