from kafka import KafkaProducer
import json
import logging

class KafkaEventProducer:
    def __init__(self, bootstrap_servers='localhost:9092'):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: str(k).encode('utf-8') if k else None
        )
        self.logger = logging.getLogger(__name__)
    
    def send_click_event(self, click_event):
        try:
            future = self.producer.send(
                'product-clicks',
                key=str(click_event.product_id),
                value=click_event.to_dict()
            )
            self.producer.flush()
            self.logger.info(f"Sent click event: {click_event.to_dict()}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to send click event: {e}")
            return False
    
    def close(self):
        self.producer.close()