from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment
from pyflink.datastream.connectors import FlinkKafkaConsumer
from pyflink.common.serialization import SimpleStringSchema
from pyflink.common.typeinfo import Types
import json
import redis
import logging

class FlinkRecommendationProcessor:
    def __init__(self):
        self.env = StreamExecutionEnvironment.get_execution_environment()
        self.env.set_parallelism(1)
        
        # Redis connection for real-time updates
        self.redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def create_kafka_source(self):
        """Create Kafka source for consuming click events"""
        kafka_props = {
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'flink-recommendation-processor'
        }
        
        kafka_consumer = FlinkKafkaConsumer(
            topics=['product-clicks'],
            deserialization_schema=SimpleStringSchema(),
            properties=kafka_props
        )
        kafka_consumer.set_start_from_latest()
        
        return kafka_consumer
    
    def process_click_events(self):
        """Process click events and update recommendations in real-time"""
        # Create Kafka source
        kafka_source = self.create_kafka_source()
        
        # Add source to environment
        click_stream = self.env.add_source(kafka_source)
        
        # Parse JSON and process events
        parsed_stream = click_stream.map(
            lambda x: json.loads(x),
            output_type=Types.PICKLED_BYTE_ARRAY()
        )
        
        # Process each click event
        processed_stream = parsed_stream.map(
            self.process_single_click,
            output_type=Types.STRING()
        )
        
        # Print results (for debugging)
        processed_stream.print()
        
        return processed_stream
    
    def process_single_click(self, click_event):
        """Process a single click event and update real-time stats"""
        try:
            product_id = str(click_event['product_id'])
            category = click_event['category']
            timestamp = click_event['timestamp']
            
            # Update Redis with real-time statistics
            self.update_realtime_stats(product_id, category, timestamp)
            
            # Update trending products
            self.update_trending_products(category, product_id)
            
            # Update recommendation weights
            self.update_recommendation_weights(product_id, category)
            
            self.logger.info(f"Processed click for product {product_id} in category {category}")
            return f"Processed: {product_id}-{category}"
            
        except Exception as e:
            self.logger.error(f"Error processing click event: {e}")
            return f"Error: {str(e)}"
    
    def update_realtime_stats(self, product_id, category, timestamp):
        """Update real-time statistics in Redis"""
        try:
            # Update category click counts
            self.redis_client.hincrby(f"category_clicks:{category}", product_id, 1)
            self.redis_client.expire(f"category_clicks:{category}", 3600)  # 1 hour TTL
            
            # Update global product popularity
            self.redis_client.zincrby("popular_products", 1, product_id)
            
            # Update recent activity
            recent_key = f"recent_activity:{int(timestamp // 300) * 300}"  # 5-minute windows
            self.redis_client.hincrby(recent_key, f"{category}:{product_id}", 1)
            self.redis_client.expire(recent_key, 900)  # 15 minutes TTL
            
        except Exception as e:
            self.logger.error(f"Error updating real-time stats: {e}")
    
    def update_trending_products(self, category, product_id):
        """Update trending products for the category"""
        try:
            # Add to trending list with current timestamp as score
            import time
            current_time = time.time()
            
            trending_key = f"trending:{category}"
            self.redis_client.zadd(trending_key, {product_id: current_time})
            
            # Keep only recent trends (last hour)
            cutoff_time = current_time - 3600
            self.redis_client.zremrangebyscore(trending_key, 0, cutoff_time)
            
            # Set expiration
            self.redis_client.expire(trending_key, 7200)  # 2 hours TTL
            
        except Exception as e:
            self.logger.error(f"Error updating trending products: {e}")
    
    def update_recommendation_weights(self, product_id, category):
        """Update recommendation weights based on real-time data"""
        try:
            # Update co-occurrence matrix (products viewed together)
            recent_views_key = "recent_user_views"
            
            # Get recent views (simplified - in production, you'd track user sessions)
            recent_views = self.redis_client.lrange(recent_views_key, 0, 10)
            
            # Update co-occurrence for each recent view
            for recent_product in recent_views:
                if recent_product != product_id:
                    cooccur_key = f"cooccur:{min(product_id, recent_product)}:{max(product_id, recent_product)}"
                    self.redis_client.incr(cooccur_key)
                    self.redis_client.expire(cooccur_key, 3600)
            
            # Add current product to recent views
            self.redis_client.lpush(recent_views_key, product_id)
            self.redis_client.ltrim(recent_views_key, 0, 50)  # Keep last 50 views
            self.redis_client.expire(recent_views_key, 1800)  # 30 minutes TTL
            
        except Exception as e:
            self.logger.error(f"Error updating recommendation weights: {e}")
    
    def run(self):
        """Run the Flink job"""
        try:
            self.logger.info("Starting Flink recommendation processor...")
            self.process_click_events()
            self.env.execute("Real-time Recommendation Processor")
        except Exception as e:
            self.logger.error(f"Error running Flink job: {e}")

if __name__ == "__main__":
    processor = FlinkRecommendationProcessor()
    processor.run()
    