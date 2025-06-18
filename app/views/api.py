from flask import Blueprint, render_template
from app.controllers.recommendation_controller import RecommendationController

api_bp = Blueprint('api', __name__)
controller = RecommendationController()

@api_bp.route('/')
def index():
    """Render main page"""
    return render_template('index.html')

@api_bp.route('/api/products', methods=['GET'])
def get_products():
    """Get all products"""
    return controller.get_products()

@api_bp.route('/api/track-click', methods=['POST'])
def track_click():
    """Track product click"""
    return controller.track_click()

@api_bp.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    """Get recommendations"""
    return controller.get_recommendations()