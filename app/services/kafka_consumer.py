from kafka import KafkaConsumer
import json
import logging
from threading import Thread

class KafkaEventConsumer:
    def __init__(self, bootstrap_servers='localhost:9092', group_id='recommendation-group'):
        self.consumer = KafkaConsumer(
            'product-clicks',
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda v: json.loads(v.decode('utf-8')),
            key_deserializer=lambda k: k.decode('utf-8') if k else None,
            auto_offset_reset='latest'
        )
        self.logger = logging.getLogger(__name__)
        self.running = False
    
    def start_consuming(self, callback):
        self.running = True
        thread = Thread(target=self._consume_messages, args=(callback,))
        thread.daemon = True
        thread.start()
        return thread
    
    def _consume_messages(self, callback):
        try:
            for message in self.consumer:
                if not self.running:
                    break
                click_event = message.value
                self.logger.info(f"Received click event: {click_event}")
                callback(click_event)
        except Exception as e:
            self.logger.error(f"Error consuming messages: {e}")
    
    def stop(self):
        self.running = False
        self.consumer.close()