# SDR Real-Time Recommendation System

A high-performance, real-time recommendation system built with gRPC, Kafka, and Flask, designed to provide intelligent product recommendations based on user behavior and content similarity.

## 🚀 Features

- **Real-time Recommendations**: Instant product suggestions based on user interactions
- **Content-Based Filtering**: TF-IDF and cosine similarity for product matching
- **Category Trending**: Dynamic recommendations based on popular products in categories
- **gRPC Communication**: High-performance inter-service communication
- **Kafka Integration**: Real-time event streaming and processing
- **Redis Caching**: Fast in-memory data storage for click statistics
- **Docker Support**: Easy deployment and scaling
- **RESTful API**: Clean HTTP endpoints for integration

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Client    │    │   gRPC Client   │    │   Kafka Client  │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          ▼                      ▼                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Flask Web Application                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │   REST API  │  │ gRPC Server │  │   Kafka Consumer       │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
└─────────────────────────┬───────────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
┌─────────────────┐ ┌─────────────┐ ┌─────────────┐
│   Redis Cache   │ │  Kafka     │ │  Models     │
│                 │ │  Producer  │ │             │
└─────────────────┘ └─────────────┘ └─────────────┘
```

## 📁 Project Structure

```
sdr_proj/
├── app/
│   ├── controllers/          # Business logic controllers
│   ├── models/              # Data models and database
│   ├── protos/              # Protocol Buffer definitions
│   ├── services/            # Core business services
│   ├── templates/           # HTML templates
│   ├── views/               # API route definitions
│   └── __init__.py
├── docker-compose.yml       # Multi-service orchestration
├── Dockerfile              # Application containerization
├── main.py                 # Application entry point
└── requirements.txt        # Python dependencies
```

## 🛠️ Technology Stack

- **Backend**: Python 3.8+, Flask
- **Communication**: gRPC, Protocol Buffers
- **Message Queue**: Apache Kafka
- **Caching**: Redis
- **ML Libraries**: scikit-learn, NumPy
- **Containerization**: Docker, Docker Compose
- **API**: RESTful HTTP endpoints

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.8 or higher
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/younesskellal1/real-time-recommendation-system.git
cd real-time-recommendation-system
```

### 2. Start Services with Docker

```bash
docker-compose up -d
```

This will start:
- **Zookeeper** (port 2181)
- **Kafka** (port 9092)
- **Redis** (port 6379)
- **Recommendation App** (port 5000)

### 3. Access the Application

- **Web Interface**: http://localhost:5000
- **API Endpoints**: http://localhost:5000/api/
- **gRPC Server**: localhost:50051

## 📚 API Documentation

### REST API Endpoints

#### Get Product Recommendations

```http
GET /api/recommendations/{product_id}?limit={limit}
```

**Parameters:**
- `product_id` (path): ID of the product to get recommendations for
- `limit` (query): Maximum number of recommendations (default: 5)

**Response:**
```json
{
  "recommendations": [
    {
      "product": {
        "id": 2,
        "name": "Product Name",
        "category": "Electronics",
        "price": 99.99,
        "rating": 4.5
      },
      "score": 0.85,
      "reason": "Similar to your viewed product"
    }
  ]
}
```

#### Get All Products

```http
GET /api/products
```

**Response:**
```json
{
  "products": [
    {
      "id": 1,
      "name": "Product Name",
      "category": "Electronics",
      "price": 99.99,
      "rating": 4.5,
      "tags": ["wireless", "bluetooth"],
      "description": "Product description"
    }
  ]
}
```

### gRPC Services

The system provides gRPC services for high-performance inter-service communication:

- **RecommendationService**: Get product recommendations
- **ProductService**: Product management operations
- **UserService**: User-related operations

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka broker addresses | `kafka:9092` |
| `REDIS_HOST` | Redis server host | `redis` |
| `REDIS_PORT` | Redis server port | `6379` |
| `FLASK_ENV` | Flask environment | `production` |
| `SECRET_KEY` | Flask secret key | `dev-secret-key` |

### Kafka Topics

- `product_clicks`: User click events on products
- `user_behavior`: User interaction data
- `recommendation_requests`: Recommendation generation requests

## 🧠 Recommendation Algorithm

### 1. Content-Based Filtering

Uses TF-IDF vectorization and cosine similarity to find products with similar characteristics:

```python
# Product features: category + tags + description
features = f"{category} {' '.join(tags)} {description}"

# TF-IDF vectorization
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(features)

# Cosine similarity calculation
similarity_matrix = cosine_similarity(tfidf_matrix)
```

### 2. Category Trending

Combines recent click statistics with product ratings:

```python
score = (clicks_score * 0.3) + (rating_score * 0.2)
```

### 3. Hybrid Scoring

Final recommendations combine multiple signals:
- Content similarity (80% weight)
- Category trending (20% weight)
- User behavior patterns

## 📊 Data Models

### Product Model

```python
class Product:
    id: int
    name: str
    category: str
    price: float
    rating: float
    tags: List[str]
    description: str
```

### Recommendation Model

```python
class Recommendation:
    product_id: int
    score: float
    reason: str
```

### User Model

```python
class User:
    id: int
    username: str
    preferences: Dict[str, Any]
    behavior_history: List[Dict]
```

## 🔄 Data Flow

1. **User Interaction**: User clicks on a product
2. **Event Generation**: Click event sent to Kafka
3. **Event Processing**: Kafka consumer processes the event
4. **Statistics Update**: Redis cache updated with click data
5. **Recommendation Generation**: ML algorithms generate new recommendations
6. **Response**: Recommendations returned to user

## 🚀 Performance Features

- **Redis Caching**: Fast access to frequently used data
- **Async Processing**: Non-blocking Kafka consumer
- **Vectorized Operations**: NumPy for efficient matrix operations
- **Connection Pooling**: Optimized database connections
- **Load Balancing**: Docker-based horizontal scaling

## 🧪 Testing

### Run Tests

```bash
# Unit tests
python -m pytest tests/

# Integration tests
python -m pytest tests/integration/

# Performance tests
python -m pytest tests/performance/
```

### Test Coverage

```bash
python -m pytest --cov=app tests/
```

## 📈 Monitoring and Logging

### Logging

The application uses structured logging with different levels:
- **INFO**: General application events
- **WARNING**: Potential issues
- **ERROR**: Error conditions
- **DEBUG**: Detailed debugging information

### Metrics

Key performance indicators:
- Recommendation generation latency
- Kafka message processing rate
- Redis cache hit ratio
- API response times

## 🔒 Security

- **Input Validation**: All user inputs are validated
- **Rate Limiting**: API rate limiting to prevent abuse
- **CORS Configuration**: Cross-origin resource sharing setup
- **Environment Variables**: Sensitive configuration externalized

## 🚀 Deployment

### Production Deployment

1. **Environment Setup**
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-secure-secret-key
   ```

2. **Docker Production Build**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Load Balancer Configuration**
   - Configure Nginx or HAProxy
   - Set up SSL certificates
   - Configure health checks

### Scaling

- **Horizontal Scaling**: Multiple application instances
- **Kafka Partitioning**: Parallel message processing
- **Redis Clustering**: Distributed caching
- **Database Sharding**: Data distribution across nodes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Youness Kellal** - *Initial work* - [younesskellal1](https://github.com/younesskellal1)

## 🙏 Acknowledgments

- Apache Kafka community for streaming platform
- Redis team for in-memory data store
- gRPC team for high-performance communication
- scikit-learn team for machine learning tools

## 📞 Support

For support and questions:
- Create an issue in the GitHub repository
- Contact: younesskellal1@gmail.com

## 🔮 Roadmap

- [ ] Real-time user behavior analytics
- [ ] A/B testing framework for recommendations
- [ ] Machine learning model training pipeline
- [ ] GraphQL API support
- [ ] Kubernetes deployment manifests
- [ ] Advanced recommendation algorithms (collaborative filtering)
- [ ] Real-time dashboard for monitoring
- [ ] Multi-tenant support
