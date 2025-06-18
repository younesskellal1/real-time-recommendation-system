from dataclasses import dataclass
from typing import List
import time

@dataclass
class ClickEvent:
    product_id: int
    category: str
    timestamp: float
    session_id: str = None
    
    def to_dict(self):
        return {
            'product_id': self.product_id,
            'category': self.category,
            'timestamp': self.timestamp,
            'session_id': self.session_id
        }

@dataclass
class Recommendation:
    product_id: int
    score: float
    reason: str
    
    def to_dict(self):
        return {
            'product_id': self.product_id,
            'score': self.score,
            'reason': self.reason
        }